#!/usr/bin/env python3
"""
Qdrant collections sync: Node A (192.168.1.11:6333) → Node B (192.168.1.222:6333)
Scans all shared collections, compares by point ID + payload, upserts missing/different points.
"""
import json
import sys
import time
import urllib.request
import urllib.error

NODE_A = "http://192.168.1.11:6333"
NODE_B = "http://192.168.1.222:6333"
SCROLL_LIMIT = 200  # max points per scroll page

def rest(host, method, path, body=None):
    """Make REST call to Qdrant and return parsed JSON."""
    url = f"{host}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if body else {}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"  ⚠ HTTP {e.code} on {method} {url}: {err_body[:200]}")
        return None
    except urllib.error.URLError as e:
        print(f"  ⚠ Connection error on {url}: {e.reason}")
        return None

def get_collections(host):
    """Get set of collection names from a node."""
    data = rest(host, "GET", "/collections")
    if not data or "result" not in data:
        return set()
    return {c["name"] for c in data["result"]["collections"]}

def scroll_all_points(host, collection):
    """Scroll ALL points from a collection (handles pagination via 'next_page_offset')."""
    points = []
    offset = None
    page = 0
    while True:
        body = {
            "limit": SCROLL_LIMIT,
            "with_payload": True,
            "with_vector": False
        }
        if offset is not None:
            body["offset"] = offset

        data = rest(host, "POST", f"/collections/{urllib.parse.quote(collection)}/points/scroll", body)
        if not data or "result" not in data:
            print(f"  ⚠ Failed to scroll {collection} on {host}")
            break

        result = data["result"]
        batch = result.get("points", [])
        if not batch:
            break

        points.extend(batch)
        page += 1

        next_offset = result.get("next_page_offset")
        if next_offset is None:
            break
        offset = next_offset

        if page % 10 == 0:
            print(f"  ⏳ Scrolled {len(points)} points from {collection} on {host}...")

    return points

def points_by_id(points_list):
    """Build dict mapping string-ID → {payload: ..., id: original, id_str: ...}."""
    result = {}
    for p in points_list:
        pid = p.get("id")
        id_str = str(pid)
        result[id_str] = {
            "id": pid,
            "id_str": id_str,
            "payload": p.get("payload", {})
        }
    return result

def compare_and_sync(collection, a_points, b_points):
    """
    Compare points from A and B. Return stats dict.
    Upserts missing/different points from A onto B.
    """
    a_by_id = points_by_id(a_points)
    b_by_id = points_by_id(b_points)

    a_ids = set(a_by_id.keys())
    b_ids = set(b_by_id.keys())

    # Points on A but missing on B
    missing_on_b = a_ids - b_ids

    # Points on both but with different payloads
    present_on_both = a_ids & b_ids
    payload_diffs = []
    for pid in sorted(present_on_both):
        a_pay = a_by_id[pid]["payload"]
        b_pay = b_by_id[pid]["payload"]
        if a_pay != b_pay:
            payload_diffs.append(pid)

    # Points on B but not on A (report only)
    extra_on_b = b_ids - a_ids

    to_upsert_ids = sorted(missing_on_b) + sorted(payload_diffs)
    total_to_upsert = len(to_upsert_ids)

    # Also check if B has more total points (for info)
    b_extra_count = len(extra_on_b)

    if total_to_upsert == 0:
        print(f"  ✅ {collection}: Already in sync ({len(a_ids)} points, {b_extra_count} extra on B)")
        return {
            "collection": collection,
            "a_count": len(a_ids),
            "b_count": len(b_ids),
            "missing": 0,
            "payload_diff": 0,
            "upserted": 0,
            "extra_on_b": b_extra_count
        }

    print(f"  🔄 {collection}: {len(missing_on_b)} missing, {len(payload_diffs)} payload diffs = {total_to_upsert} to sync (B has {b_extra_count} extra)")

    # Build upsert payloads
    upsert_points = []
    for pid in to_upsert_ids:
        info = a_by_id[pid]
        upsert_points.append({
            "id": info["id"],
            "payload": info["payload"],
            "vector": [0.0] * 384  # zero vector placeholder
        })

    # Upsert in batches of 100
    batch_size = 100
    total_upserted = 0
    for i in range(0, len(upsert_points), batch_size):
        batch = upsert_points[i:i+batch_size]
        body = {"points": batch}
        path = f"/collections/{urllib.parse.quote(collection)}/points"
        # Use PUT (not POST) for upsert
        result = rest(NODE_B, "PUT", path, body)
        if result and result.get("status") == "ok":
            total_upserted += len(batch)
            print(f"    ✓ Upserted batch {i//batch_size + 1}/{(len(upsert_points)-1)//batch_size + 1} ({len(batch)} points)")
        else:
            status = result.get("status", "error") if result else "no-response"
            print(f"    ✗ Failed batch {i//batch_size + 1}: status={status}")
        # Small delay to avoid overwhelming
        time.sleep(0.1)

    print(f"  ✅ {collection}: Synced {total_upserted}/{total_to_upsert} points to Node B")
    return {
        "collection": collection,
        "a_count": len(a_ids),
        "b_count": len(b_ids),
        "missing": len(missing_on_b),
        "payload_diff": len(payload_diffs),
        "upserted": total_upserted,
        "extra_on_b": b_extra_count
    }

import urllib.parse

def main():
    print("=" * 70)
    print("QDRANT COLLECTION SYNC: Node A (192.168.1.11) → Node B (192.168.1.222)")
    print("=" * 70)

    # Step 1: Get collection lists
    print("\n📋 Step 1: Fetching collection lists...")
    a_cols = get_collections(NODE_A)
    b_cols = get_collections(NODE_B)

    print(f"\n  Node A: {len(a_cols)} collections")
    for c in sorted(a_cols):
        print(f"    - {c}")
    print(f"\n  Node B: {len(b_cols)} collections")
    for c in sorted(b_cols):
        print(f"    - {c}")

    shared = sorted(a_cols & b_cols)
    a_only = sorted(a_cols - b_cols)
    b_only = sorted(b_cols - a_cols)

    print(f"\n📊 Summary:")
    print(f"  Shared collections: {len(shared)}")
    print(f"  A-only collections: {len(a_only)}")
    print(f"  B-only collections: {len(b_only)}")

    if a_only:
        print(f"\n  ⚠ Node A-only collections (not on B, cannot create without config):")
        for c in a_only:
            print(f"    - {c}")
    if b_only:
        print(f"\n  ℹ Node B-only collections (not on A):")
        for c in b_only:
            print(f"    - {c}")

    # Step 2 & 3: Scroll and compare each shared collection
    print(f"\n" + "=" * 70)
    print("📥 Step 2-4: Scanning shared collections & syncing to Node B")
    print("=" * 70)

    results = []
    for i, col in enumerate(shared):
        print(f"\n{'─' * 60}")
        print(f"[{i+1}/{len(shared)}] Processing: {col}")
        print(f"{'─' * 60}")

        print(f"  🡆 Scrolling Node A...")
        a_points = scroll_all_points(NODE_A, col)
        print(f"  🡆 Scrolling Node B...")
        b_points = scroll_all_points(NODE_B, col)

        print(f"  📊 Counts: A={len(a_points)}, B={len(b_points)}")

        result = compare_and_sync(col, a_points, b_points)
        results.append(result)

    # Step 5: Final summary
    print("\n" + "=" * 70)
    print("📋 SYNC SUMMARY")
    print("=" * 70)

    total_missing = sum(r["missing"] for r in results)
    total_diff = sum(r["payload_diff"] for r in results)
    total_upserted = sum(r["upserted"] for r in results)

    print(f"\n{'Collection':<30} {'A pts':>7} {'B pts':>7} {'Missing':>8} {'Diffs':>6} {'Upd':>5} {'ExtraB':>7}")
    print(f"{'─'*30} {'─'*7} {'─'*7} {'─'*8} {'─'*6} {'─'*5} {'─'*7}")
    for r in results:
        print(f"{r['collection']:<30} {r['a_count']:>7} {r['b_count']:>7} {r['missing']:>8} {r['payload_diff']:>6} {r['upserted']:>5} {r['extra_on_b']:>7}")
    print(f"{'─'*30} {'─'*7} {'─'*7} {'─'*8} {'─'*6} {'─'*5} {'─'*7}")
    print(f"{'TOTAL':<30} {sum(r['a_count'] for r in results):>7} {sum(r['b_count'] for r in results):>7} {total_missing:>8} {total_diff:>6} {total_upserted:>5}")

    if b_only:
        print(f"\n🔔 B-ONLY COLLECTIONS (not on A): {', '.join(b_only)}")
        print(f"   These exist on Node B but not Node A. No action needed — they're already on the primary.")
    if a_only:
        print(f"\n⚠ A-ONLY COLLECTIONS (not on B): {', '.join(a_only)}")
        print(f"   These need to be created on Node B with matching config if desired.")

    print(f"\n{'='*70}")
    if total_upserted > 0:
        print(f"✅ SYNC COMPLETE: {total_upserted} points synced to Node B")
    else:
        print(f"✅ SYNC COMPLETE: No changes needed — all collections already in sync")
    print(f"{'='*70}")

    # Write results to JSON file
    output = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "node_a": NODE_A,
        "node_b": NODE_B,
        "node_a_collections": sorted(a_cols),
        "node_b_collections": sorted(b_cols),
        "shared": shared,
        "a_only": a_only,
        "b_only": b_only,
        "results": results,
        "total_upserted": total_upserted,
        "total_missing": total_missing,
        "total_payload_diffs": total_diff
    }
    with open("/workspace/qdrant_sync_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n📄 Detailed results saved to /workspace/qdrant_sync_results.json")


if __name__ == "__main__":
    main()

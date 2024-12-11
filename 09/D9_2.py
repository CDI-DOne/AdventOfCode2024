def parse_disk_map(disk_map: str):
    """
    Parse the disk map into a list of blocks.
    File blocks are strings of their file_id and free blocks are '.'.
    """
    disk = []
    file_id = 0
    for i, length in enumerate(map(int, disk_map)):
        if i % 2 == 0:  # file segment
            disk.extend([str(file_id)] * length)
            file_id += 1
        else:  # free space segment
            disk.extend(['.'] * length)
    return disk

def compute_checksum(disk):
    """Compute checksum = sum(pos * file_id) for all file blocks."""
    return sum(pos * int(block) for pos, block in enumerate(disk) if block != '.')

def compact_blocks(disk):
    n = len(disk)
    left_gap = 0
    right_block = n - 1

    while True:
        # Move left_gap to next '.' or break if none
        while left_gap < n and disk[left_gap] != '.':
            left_gap += 1
        if left_gap >= n:
            break

        # Move right_block to next file block from right
        while right_block >= 0 and disk[right_block] == '.':
            right_block -= 1
        if right_block <= left_gap:
            break

        # Swap
        disk[left_gap], disk[right_block] = disk[right_block], disk[left_gap]

    return disk

def get_file_positions(disk):
    """
    Return a dict mapping file_id (as string) to (start_position, length).
    """
    file_map = {}
    start = None
    current_id = None
    for i, block in enumerate(disk):
        if block == '.':
            if current_id is not None:
                file_map[current_id] = (start, i - start)
                current_id = None
        else:
            if block != current_id:
                if current_id is not None:
                    file_map[current_id] = (start, i - start)
                current_id = block
                start = i
    if current_id is not None:
        file_map[current_id] = (start, len(disk) - start)
    return file_map

def get_free_segments(disk):
    """
    Identify and return a list of free segments as (start, length).
    """
    free_segments = []
    n = len(disk)
    i = 0
    while i < n:
        if disk[i] == '.':
            start = i
            while i < n and disk[i] == '.':
                i += 1
            length = i - start
            free_segments.append((start, length))
        else:
            i += 1
    return free_segments

def find_and_use_free_segment(free_segments, end_pos, length_needed):
    """
    Given a sorted list of free segments (start, length) and the required length_needed,
    find the first free segment entirely to the left of end_pos that can fit length_needed.
    If found, update that segment (or remove it if fully used) and return start position.
    Otherwise, return None.
    """
    for idx, (seg_start, seg_length) in enumerate(free_segments):
        # The free segment must lie before end_pos:
        # Actually, only the start of the segment needs to be < end_pos

        if seg_start + length_needed <= end_pos:
            if seg_length >= length_needed:
                # Use this segment
                chosen_start = seg_start
                # Update or remove the segment
                new_start = seg_start + length_needed
                new_length = seg_length - length_needed
                if new_length > 0:
                    free_segments[idx] = (new_start, new_length)
                else:
                    # Entire segment used
                    del free_segments[idx]
                return chosen_start
    return None

def compact_files_whole(disk):
    # Precompute file positions and free segments
    file_map = get_file_positions(disk)
    free_segments = get_free_segments(disk)

    # Sort files by file_id descending
    file_ids = sorted(file_map.keys(), key=lambda x: int(x), reverse=True)

    for file_id in file_ids:
        start, length = file_map[file_id]
        seg_start = find_and_use_free_segment(free_segments, start, length)
        if seg_start is not None:
            # Move the file here
            for i in range(start, start + length):
                disk[i] = '.'
            for i in range(seg_start, seg_start + length):
                disk[i] = file_id
            # Update file_map so it's consistent if needed later
            file_map[file_id] = (seg_start, length)

    return disk

if __name__ == "__main__":
    with open("Input.txt", "r") as f:
        disk_map_input = f.read().strip()

    # Part 1
    disk_part1 = parse_disk_map(disk_map_input)
    compacted_part1 = compact_blocks(disk_part1)
    checksum_part1 = compute_checksum(compacted_part1)
    print("Part 1 Checksum:", checksum_part1)

    # Part 2
    disk_part2 = parse_disk_map(disk_map_input)
    compacted_part2 = compact_files_whole(disk_part2)
    checksum_part2 = compute_checksum(compacted_part2)
    print("Part 2 Checksum:", checksum_part2)

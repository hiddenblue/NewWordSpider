import filecmp
import shutil

def compare_and_merge_files(old_file, new_file, merged_file):
    # 对比文件内容
    if filecmp.cmp(old_file, new_file):
        # 如果文件内容相同，直接使用旧文件
        shutil.copyfile(old_file, merged_file)
    else:
        # 如果文件内容不同，合并文件
        with open(old_file, 'r') as old, open(new_file, 'r') as new, open(merged_file, 'w') as merged:
            old_lines = set(old.readlines())
            new_lines = set(new.readlines())
            merged_lines = old_lines.union(new_lines)
            merged.writelines(merged_lines)

if __name__ == "__main__":
    import sys
    old_file = sys.argv[1]
    new_file = sys.argv[2]
    merged_file = sys.argv[3]
    compare_and_merge_files(old_file, new_file, merged_file)
import glob
import io
import sys
import tokenize


def remove_comments_from_source(source_code):
    tokens = []
    try:
        for tokinfo in tokenize.generate_tokens(io.StringIO(source_code).readline):
            if tokinfo.type != tokenize.COMMENT:
                tokens.append(tokinfo)
    except tokenize.TokenError as e:
        raise Exception(f"TokenError: {e}") from e

    try:
        return tokenize.untokenize(tokens)
    except Exception as e:
        final_token_line = "unknown"
        if tokens:
            final_token_line = str(tokens[-1].start[0])
        raise Exception(f"UntokenizeError: {e} near line {final_token_line}") from e


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_python_comments.py <file_glob_pattern>", file=sys.stderr)
        sys.exit(1)

    file_pattern = sys.argv[1]
    file_paths = glob.glob(file_pattern)

    if not file_paths:
        print(f"No files found matching pattern: {file_pattern}", file=sys.stderr)
        sys.exit(1)

    for file_path in file_paths:
        print(f"Processing {file_path}...")
        backup_path = file_path + ".bak_claudecode"
        original_source = ""

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_source = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            continue  # Skip to the next file
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            continue  # Skip to the next file

        try:
            with open(backup_path, "w", encoding="utf-8") as f_bak:
                f_bak.write(original_source)
            print(f"  Backup: {backup_path}")
        except Exception as e:
            print(f"  Error creating backup for {file_path}: {e}", file=sys.stderr)
            continue  # Skip to the next file

        try:
            cleaned_source = remove_comments_from_source(original_source)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_source)
            print(f"  Comments removed: {file_path}")

        except Exception as e:
            print(f"  Processing Error for {file_path}: {e}", file=sys.stderr)
            print(f"  Restoring {file_path} from {backup_path}...", file=sys.stderr)
            try:
                with open(backup_path, "r", encoding="utf-8") as f_bak_read:
                    backup_content = f_bak_read.read()
                with open(file_path, "w", encoding="utf-8") as f_orig_write:
                    f_orig_write.write(backup_content)
                print(f"  Restored: {file_path} from {backup_path}.", file=sys.stderr)
            except Exception as restore_e:
                print(
                    f"  CRITICAL: Restore failed for {file_path}. Backup is at {backup_path}. Error: {restore_e}",
                    file=sys.stderr,
                )
            # Continue to the next file even if one fails

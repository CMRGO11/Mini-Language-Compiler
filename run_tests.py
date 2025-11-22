import os
import subprocess

# Paths
COMPILER = "src/compilador.py"
TESTS_ROOT = "src/tests"

def run_test(file_path):
    print("\n-------------------------------------------")
    print(f"Running test: {file_path}")
    print("-------------------------------------------")

    try:
        # Execute compiler
        result = subprocess.run(
            ["python", COMPILER, file_path],
            capture_output=True,
            text=True
        )

        # Print compiler output
        print(result.stdout)

        # Check for errors
        if result.returncode != 0:
            print(f"[FAIL ❌] {file_path}")
            print(result.stderr)
            return False

        print(f"[PASS ✅] {file_path}")
        return True

    except Exception as e:
        print(f"[CRASH ❌] {file_path}")
        print("Error:", e)
        return False


def run_all_tests():
    total = 0
    passed = 0

    print("\n===========================================")
    print("          Mini Language Test Suite")
    print("===========================================\n")

    # Walk through all subfolders in tests/
    for root, _, files in os.walk(TESTS_ROOT):
        for filename in files:
            if filename.endswith(".txt"):
                total += 1
                test_path = os.path.join(root, filename)

                if run_test(test_path):
                    passed += 1

    # Summary
    print("\n===========================================")
    print("                 SUMMARY")
    print("===========================================\n")
    print(f"Total tests:  {total}")
    print(f"Passed:       {passed}")
    print(f"Failed:       {total - passed}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!\n")
    else:
        print("\n❗ Some tests failed. Review the output above.\n")


if __name__ == "__main__":
    run_all_tests()

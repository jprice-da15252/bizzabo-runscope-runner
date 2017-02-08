import requests
import sys
import time

def main():
    trigger_url = sys.argv[1]
    trigger_resp = requests.get(trigger_url)

    if trigger_resp.ok:
        trigger_json = trigger_resp.json().get("data", {})

        test_runs = trigger_json.get("runs", [])

        print "Started {} test runs.".format(len(test_runs))

        results = {}
        while len(results.keys()) < len(test_runs):
            time.sleep(1)

            for run in test_runs:
                test_run_id = run.get("test_run_id")
                if not test_run_id in results:
                    result = _get_result(run)
                    if result.get("result") in ["pass", "fail"]:
                        results[test_run_id] = result

        pass_count = sum([r.get("result") == "pass" for r in results.values()])
        fail_count = sum([r.get("result") == "fail" for r in results.values()])

        if fail_count > 0:
            print "{} test runs passed. {} test runs failed.".format(pass_count, fail_count)
            exit(1)

        print "All test runs passed."


def _get_result(test_run):
    # generate Personal Access Token at https://www.runscope.com/applications
    API_TOKEN = "xxxxxxxxxxxxxxxxxxxx"

    opts = {
        "base_url": "https://api.runscope.com",
        "bucket_key": test_run.get("bucket_key"),
        "test_id": test_run.get("test_id"),
        "test_run_id": test_run.get("test_run_id")
    }
    result_url = "{base_url}/buckets/{bucket_key}/tests/{test_id}/results/{test_run_id}".format(**opts)
    print "Getting result: {}".format(result_url)
    result_resp = requests.get(result_url, headers={"Authorization":"Bearer {}".format(API_TOKEN)})

    if result_resp.ok:
        return result_resp.json().get("data")

    return None


if __name__ == '__main__':
    main()
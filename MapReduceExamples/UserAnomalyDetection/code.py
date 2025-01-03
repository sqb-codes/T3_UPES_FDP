from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
from collections import defaultdict

class AnomalousDetection(MRJob):
    def steps(self):
        return [
            MRStep(mapper = self.mapper_parse_logs,
                   reducer = self.reducer_agg_stats),
            MRStep(reducer=self.reducer_identify_suspicious)
        ]

    def mapper_parse_logs(self, _, line):
        try:
            timestamp, userId, url, response_code, response_time = line.split()
            response_code = int(response_code)
            response_time = int(response_time)

            hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H")
            yield userId, (1, response_code != 200, response_time, hour)
        except BaseException as ex:
            pass

    def reducer_agg_stats(self, user_id, values):
        total_requests = 0
        failed_requests = 0
        total_response_time = 0
        hourly_count = defaultdict(int)

        for count, is_failure, response_time, hour in values:
            total_requests += count
            failed_requests += is_failure
            total_response_time += response_time
            hourly_count[hour] += 1

        yield user_id, {
            "total_requests" : total_requests,
            "failed_requests" : failed_requests,
            "total_response_time" : total_response_time,
            "hourly_counts" : dict(hourly_count)
        }

    def reducer_identify_suspicious(self, user_id, agg_stats):
        for stats in agg_stats:
            total_requests = stats["total_requests"]
            failed_requests = stats["failed_requests"]
            total_response_time = stats["total_response_time"]
            hourly_count = stats["hourly_counts"]

            failure_rate = failed_requests / total_requests
            avg_response_time = total_response_time / total_requests
            max_req_count = max(hourly_count, key=hourly_count.get)

            anomalies = []
            if failure_rate >= 0.5:
                anomalies.append("High Failure Rate")
            if total_requests > 1000:
                anomalies.append("Excessive Reuqest Rate")
            if avg_response_time > 500:
                anomalies.append("Slow Requests")

            if anomalies:
                yield user_id, {
                    "anomalies" : anomalies,
                    "total_requests": total_requests,
                    "failure_rate": f"{failure_rate:.2%}",
                    "avg_response_time": f"{avg_response_time:.2f} ms",
                    "max_request_hour": max_req_count
                }

AnomalousDetection.run()
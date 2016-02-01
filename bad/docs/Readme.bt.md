# Brief guide

“httpget” & “udpjitter” for march & april 2014.

This was just a select * from … (so haven’t enclosed that data!). We have some issues we know about, no doubt there are some we don’t – we can compare with what you find!!.

List of units on a trial (at 30th april) ~90 probes.  Results from these probes should be ignored (can ignore http/udp data for those probes).
 
Metadata for those probes whose metadata didn’t change during march and april (although our DB only goes back to start of april, sam has the earlier data & pulled the info). Metadata is RAN, AP, hub type and headline speed – all anonymised. You’ll find some results for other probes - ~300 whose metadata did change (can ignore http/udp data for those probes)
 
 
# Data format
## curr_udpjitter.csv
--------------------------------------------------------------------
unit_id			- Unique identifier for an individual unit
dtime			- Time test finished in UTC
target			- Target hostname or IP address
packet_size		- Size of each UDP Datagram (Units: Bytes)
stream_rate		- Rate at which the UDP stream is generated (Units: bits/sec)
duration		- Total duration of test (Units: microseconds)
packets_up_sent		- Number of packets sent in Upstream (measured by client)
packets_down_sent	- Number of packets sent in Downstream (measured by server)
packets_up_recv		- Number of packets received in Upstream (measured by server)
packets_down_recv	- Number of packets received in Downstream (measured by client)
jitter_up		- Upstream Jitter measured (Units: microseconds)
jitter_down		- Downstream Jitter measured (Units microseconds)
latency			- 99th percentile of round trip times for all packets
successes		- Number of successes (always 1 or 0 for this test)
failures		- Number of failures (always 1 or 0 for this test)
location_id		- Please ignore (this is an internal key mapping to unit profile data)
 
 
## curr_httpgetmt.csv
--------------------------------------------------------------------
unit_id			- Unique identifier for an individual unit
dtime			- Time test finished in UTC
target			- Target hostname or IP address
address			- The IP address of the server (resolved by the client's DNS)
fetch_time		- Time the test ran for in microseconds
bytes_total		- Total bytes downloaded across all connections
bytes_sec		- Running total of throughput, which is sum of speeds measured for each stream (in bytes/sec), from the start of the test to the current interval
bytes_sec_interval	- Throughput at this specific interval (e.g. Throughput between 25-30 seconds)
warmup_time		- Time consumed for all the TCP streams to arrive at optimal window size (Units: microseconds)
warmup_bytes		- Bytes transferred for all the TCP streams during the warm-up phase.
sequence		- The interval that this row refers to (e.g. in the US, sequence=0 implies result is for 0-5 seconds of the test)
threads			- The number of concurrent TCP connections used in the test
successes		- Number of successes (always 1 or 0 for this test)
failures		- Number of failures (always 1 or 0 for this test)
location_id		- Please ignore (this is an internal key mapping to unit profile data)
 
[this is for the multi-threaded variant – you have results for single threaded variant]
 
 
 

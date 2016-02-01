import numpy as np
import pandas as pd

cols_http_org = ['UNIT_ID',
     'DTIME',
     'TARGET',
     'ADDRESS',
     'FETCH_TIME',
     'BYTES_TOTAL',
     'BYTES_SEC',
     'BYTES_SEC_INTERVAL',
     'WARMUP_TIME',
     'WARMUP_BYTES',
     'SEQUENCE',
     'THREADS',
     'SUCCESSES',
     'FAILURES',
     'LOCATION_ID']

cols_all = ['unit_id', 'dtime', 'day', 'hour', 'minute', 'target',
          'packet_size', 'stream_rate', 'duration', 'packets_up_sent',
          'packets_down_sent', 'packets_up_recv', 'packets_down_recv',
          'jitter_up', 'jitter_down', 'latency', 'successes', 'failures',
          'location_id', 'ranNode', 'apNode', 'hubType', 'headlineSpeed']

cols_UDP_net_feat = ['unit_id', 'target', 'dtime', 'day', 'hour', 'minute',
                  'packets_up_sent', 'packets_down_sent',
                  'packets_up_recv', 'packets_down_recv', 'jitter_up',
                  'jitter_down', 'latency', 'successes', 'failures',
                  'location_id', 'ranNode', 'apNode', 'hubType',
                  'headlineSpeed']


cols_UDP_net_stats = ['packets_up_sent', 'packets_down_sent',
                    'packets_up_recv', 'packets_down_recv', 'jitter_up',
                    'jitter_down', 'latency']

    
    

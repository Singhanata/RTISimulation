"""
Created on Fri Sep 30 10:51:00 2022

@author: krong
"""
import serial
import numpy as np
import threading
from rti_frame import FrameIndex,FrameSymbol
from rti_input import RTIInput
# from rti_eval import RTIEvaluation, RecordIndex


class RTIProcess():
    RECORD_SIZE = 10
    
    def __init__(self, sim):
        setting = {
            # scenario setting
            'title': 'RTIExperiment',
            'area_dimension': (6., 6.),
            'voxel_dimension': (0.20, 0.20),
            'sensing_area_position': (6., 6.),
            'n_sensor':2,
            'alpha': 1,
            'schemeType': 'SW',
            'weightalgorithm': 'EX',
            # 'object_dimension': (0.5, 0.5),
            'object_type': 'human',
            # sample setting
            'SNR': 4,
            'SNR_mode': 2,
            # 'sample_size' : 100,
            # input setting
            # 'paramset': ['obj_pos'],
            # 'paramlabel': ['Object Position'],
            # 'param1' : np.linspace(8, 64, 15),
            # 'param2' : ['LS1','LS2','EL','EX','IN'],
            # output setting
            'gfx_enabled': True
            # 'record_enabled': False,
            # 'der_plot_enabled': False,
            # 'frame_rate': 30
            # 'resultset': [
            #     RecordIndex.RMSE_ALL,
            #     RecordIndex.OBJ_RATIO,
            #     RecordIndex.DERIVATIVE_RATIO_BN]
        }

        self.savepath = sim.process_routine(**setting)
        dim = sim.getInputDimension()
        self.input = RTIInput(self.RECORD_SIZE, dim, self.savepath, 'rssi', 'ir')
        self.ready = False
        self.sUpdate = False
        self.sim = sim
        while(1):
            if self.sUpdate:
                # build image
                pass
                
    def receive_callback(self, msg):
        if msg[FrameIndex.TYPE] == FrameSymbol.CONTENT:
            self.receive_content(msg)
        elif msg[0] == 0x00:
            self.sUpdate = True
        else:
            print(msg)
    
    def receive_content(self, msg):
        msgID = int.from_bytes(msg[FrameIndex.ID])
        sNID = msg[FrameIndex.sNID]
        sDID = msg[FrameIndex.sDID]
        print('NODE ID:' + str(sDID))
        l = int.from_bytes(msg[FrameIndex.LENGTH_START:FrameIndex.MASK], 
                           "little", signed=True)
        mask = int.from_bytes(msg[FrameIndex.MASK:FrameIndex.PAYLOAD], 
                              "little", signed=True)
        if mask == FrameSymbol.MASK:
            n = int(l/2-1)
            ptr = FrameIndex.PAYLOAD
            sIDX = int(sDID - 1)
            for i in range(n):
                rssi_vl = int.from_bytes(msg[ptr:(ptr+FrameSymbol.SIZE)], 
                                         "little", signed=True)
                ptr+=FrameSymbol.SIZE
                print("RSSI: " +  str(rssi_vl))
                self.input.update(rssi_vl, 'rssi', sDID, i)
            mask = int.from_bytes(msg[ptr:(ptr+FrameSymbol.SIZE)], 
                                  "little", signed=True)
            ptr+=FrameSymbol.SIZE
            if mask == FrameSymbol.MASK:
                for i in range(n):
                    ir_vl = int.from_bytes(msg[ptr:(ptr+FrameSymbol.SIZE)], 
                                           "little", signed=True)
                    print("IR:" + str(ir_vl))
                    ptr+=FrameSymbol.SIZE
                    self.input.update(ir_vl, 'ir', sDID, i)
                mask = int.from_bytes(msg[ptr:(ptr+FrameSymbol.SIZE)], 
                                      "little", signed=True)
                ptr+=FrameSymbol.SIZE
                self.input.count[sIDX] += 1
                if mask != FrameSymbol.MASK:
                    print('END MASK not detected')
            else:
                print('IR MASK not detected')
        else:
            print('RSSI MASK not detected')
                        
class ReceiveThread(threading.Thread):
    def __init__(self, threadID, name, counter, rtiConn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.rtiConn = rtiConn

    def run(self):
        print("Starting " + self.name)
        self.rtiConn.receive()
        print("Exiting " + self.name)


class RTIConnection():
    MAX_BUFFER_SIZE = 100
    THRESHOLD_LOG_LORA_RECEIVE = 10000
    MODESTR = 'CONSISTANT_SERIAL'
    
    START_SYM = 0x01
    STOP_SYM = 0x3E
    SEPARATE_SYM = 0x3A

    TYPE_SYM = 0x54
    ID_SYM = 0x49
    SENDER_SYM = 0x53
    RECEIVER_SYM = 0x52
    NEXT_SYM = 0x58
    NODE_SYM = 0x4E
    MASK_SYM = 0x7E
    SPACE_SYM = 0x20

    TYPE_BEACON_SYM = 0x30
    TYPE_CONTENT_SYM = 0x31

    def __init__(self, listener, portStr='COM3'):
        try:
            self.conn = serial.Serial(portStr,
                                      115200,
                                      serial.EIGHTBITS,
                                      serial.PARITY_NONE,
                                      serial.STOPBITS_ONE,
                                      timeout=1)
        except:
            raise Exception('Unsuccessful COM Port connection')
        self.listener = listener

    def receive(self):
        while(1):
            if self.conn.in_waiting > 0:
                msg = self.conn.readline()
                if len(msg) > 0:
                    self.listener.receive_callback(msg, self)

        # self.histogram_log_1 = {}
        # self.histogram_log_2 = {}
        # self.input_1 = {}
        # self.input_2 = {}
        # for i in range(self.dim[0]):
        #     self.histogram_log_1[i+1] = np.zeros([self.dim[1], self.RECORD_SIZE])
        #     self.histogram_log_2[i+1] = np.zeros([self.dim[1], self.RECORD_SIZE])
        #     self.input_1[i+1] = np.zeros([self.dim[1], 2])
        #     self.input_2[i+1] = np.zeros([self.dim[1], 2])
        # self.recordCount = np.zeros(self.dim[0], dtype=int)

        # if (msg[0] == RTIConnection.START_SYM):
        #     print(msg)
        #     if (msg[1] != RTIConnection.TYPE_SYM):
        #         raise Exception("Invalid Format: Missing TYPE Character")
        #     b2 = (msg[4] == RTIConnection.TYPE_CONTENT_SYM)
        #     if b2:
        #         sender = msg[18:20].decode("utf-8")
        #         sender_idx = int(sender)
        #         print(sender)
        #         if (msg[37] != RTIConnection.MASK_SYM):
        #             raise Exception("Invalid Format: Missing MASK Character")
        #         else:
        #             # read RSSI values\
        #             i = 38
        #             while((i < len(msg)) and (msg[i] != RTIConnection.MASK_SYM)):
        #                 if msg[i] != RTIConnection.START_SYM:
        #                     if msg[i] != RTIConnection.SPACE_SYM:                                
        #                         raise Exception(
        #                             "Invalid Format: Missing START Character")
        #                     else:
        #                         i += 1
        #                 i += 2
        #                 n_idx = int(msg[i:(i+2)]) - 1
        #                 print(n_idx)
        #                 i += 2
        #                 if msg[i] != RTIConnection.SEPARATE_SYM:
        #                     raise Exception(
        #                         "Invalid Format: Missing SEPARATE Character")
        #                 i += 1
        #                 rssi_vl = 0
        #                 if msg[i] == 0x2D:
        #                     rssi_vl = int(msg[i:(i+3)])
        #                     i += 3
        #                 else:
        #                     rssi_vl = int(msg[i:(i+2)])
        #                     i += 2
        #                 print(self.recordCount[(sender_idx-1)])
        #                 self.histogram_log_1[sender_idx][n_idx][self.recordCount[(sender_idx-1)]] = rssi_vl
        #                 print(self.histogram_log_1[sender_idx][n_idx][self.recordCount[sender_idx-1]])
        #                 if msg[i] != RTIConnection.STOP_SYM:
        #                     raise Exception(
        #                         "Invalid Format: Missing STOP Character")
        #                 i += 1

        #             i += 1
        #             while(i < (len(msg)-2)):
        #                 if msg[i] != RTIConnection.START_SYM:
        #                     if msg[i] !=  RTIConnection.SPACE_SYM:
        #                         raise Exception(
        #                             "Invalid Format: Missing START Character")
        #                     else:
        #                         i += 1
        #                 i += 2
        #                 n_idx = int(msg[i:(i+2)]) - 1
        #                 print(n_idx)
        #                 i += 2
        #                 if msg[i] != RTIConnection.SEPARATE_SYM:
        #                     raise Exception(
        #                         "Invalid Format: Missing SEPARATE Character")
        #                 i += 1
        #                 ir_vl = 0
        #                 if msg[i] == 0x2D:
        #                     ir_vl = int(msg[i:(i+5)])
        #                     i += 5
        #                 else:
        #                     ir_vl = int(msg[i:(i+4)])
        #                     i += 4
        #                 self.histogram_log_2[sender_idx][n_idx][self.recordCount[sender_idx-1]] = ir_vl
        #                 print(self.histogram_log_2[sender_idx][n_idx][self.recordCount[sender_idx-1]])
        #                 if msg[i] != RTIConnection.STOP_SYM:
        #                     raise Exception(
        #                         "Invalid Format: Missing STOP Character")
        #                 i += 1
        #             self.recordCount[sender_idx-1] += 1
        #             print(self.recordCount[sender_idx-1])
        #             if self.recordCount[sender_idx-1] >= self.RECORD_SIZE:
        #                 self.timeStr = datetime.now().strftime('_%d%m%Y_%H%M%S')
        #                 filename = 'RSSI N' + str(sender_idx) + self.timeStr + '.csv'
        #                 filepath = os.sep.join([self.savepath['rec'], filename])
        #                 np.savetxt(filepath, self.histogram_log_1[sender_idx], delimiter = ',', fmt = '%s')
        #                 filename = 'IR N' + str(sender_idx) + self.timeStr + '.csv'
        #                 filepath = os.sep.join([self.savepath['rec'], filename])
        #                 np.savetxt(filepath, self.histogram_log_2[sender_idx], delimiter = ',', fmt = '%s')
        #                 self.recordCount[sender_idx-1] = 0

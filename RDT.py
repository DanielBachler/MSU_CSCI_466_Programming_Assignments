import Network
import argparse
from time import sleep
import hashlib


class Packet:
    ## the number of bytes used to store packet length
    seq_num_S_length = 10
    length_S_length = 10
    ## length of md5 checksum in hex
    checksum_length = 32 
        
    def __init__(self, seq_num, msg_S):
        self.seq_num = seq_num
        self.msg_S = msg_S
        
    @classmethod
    def from_byte_S(self, byte_S):
        if Packet.corrupt(byte_S):
            raise RuntimeError('Cannot initialize Packet: byte_S is corrupt')
        #extract the fields
        seq_num = int(byte_S[Packet.length_S_length : Packet.length_S_length+Packet.seq_num_S_length])
        msg_S = byte_S[Packet.length_S_length+Packet.seq_num_S_length+Packet.checksum_length :]
        return self(seq_num, msg_S)
        
        
    def get_byte_S(self):
        #convert sequence number of a byte field of seq_num_S_length bytes
        seq_num_S = str(self.seq_num).zfill(self.seq_num_S_length)
        #convert length to a byte field of length_S_length bytes
        length_S = str(self.length_S_length + len(seq_num_S) + self.checksum_length + len(self.msg_S)).zfill(self.length_S_length)
        #compute the checksum
        checksum = hashlib.md5((length_S+seq_num_S+self.msg_S).encode('utf-8'))
        checksum_S = checksum.hexdigest()
        #compile into a string
        return length_S + seq_num_S + checksum_S + self.msg_S
   
    
    @staticmethod
    def corrupt(byte_S):
        #extract the fields
        length_S = byte_S[0:Packet.length_S_length]
        seq_num_S = byte_S[Packet.length_S_length : Packet.seq_num_S_length+Packet.seq_num_S_length]
        checksum_S = byte_S[Packet.seq_num_S_length+Packet.seq_num_S_length : Packet.seq_num_S_length+Packet.length_S_length+Packet.checksum_length]
        msg_S = byte_S[Packet.seq_num_S_length+Packet.seq_num_S_length+Packet.checksum_length :]
        
        #compute the checksum locally
        checksum = hashlib.md5(str(length_S+seq_num_S+msg_S).encode('utf-8'))
        computed_checksum_S = checksum.hexdigest()
        #and check if the same
        return checksum_S != computed_checksum_S
        

class RDT:
    ## latest sequence number used in a packet
    seq_num = 1
    ## buffer of bytes read from network
    byte_buffer = '' 

    def __init__(self, role_S, server_S, port):
        self.network = Network.NetworkLayer(role_S, server_S, port)
    
    def disconnect(self):
        self.network.disconnect()
        
    def rdt_1_0_send(self, msg_S):
        p = Packet(self.seq_num, msg_S)
        self.seq_num += 1
        self.network.udt_send(p.get_byte_S())
        
    def rdt_1_0_receive(self):
        ret_S = None
        byte_S = self.network.udt_receive()
        self.byte_buffer += byte_S
        #keep extracting packets - if reordered, could get more than one
        while True:
            #check if we have received enough bytes
            if(len(self.byte_buffer) < Packet.length_S_length):
                return ret_S #not enough bytes to read packet length
            #extract length of packet
            length = int(self.byte_buffer[:Packet.length_S_length])
            if len(self.byte_buffer) < length:
                return ret_S #not enough bytes to read the whole packet
            #create packet from buffer content and add to return string
            p = Packet.from_byte_S(self.byte_buffer[0:length])
            ret_S = p.msg_S if (ret_S is None) else ret_S + p.msg_S
            #remove the packet bytes from the buffer
            self.byte_buffer = self.byte_buffer[length:]
            #if this was the last packet, will return on the next iteration
        return ret_S
    #Sent RDT 2.1 Message
    def rdt_2_1_send(self, msg_S):
        #Create Packet and sequence number
        packet = Packet(self.seq_num, msg_S)
        seq = self.seq_num
        count = 0
        #check to make sure sequence is not corrupted while sending message
        while seq == self.seq_num:
            print("Packet")
            print(packet.get_byte_S())
            self.network.udt_send(packet.get_byte_S())
            response = ''
            #Wait for response
            while response == '':
                response = self.network.udt_receive()
            print(response)
            #Recieved length of message message
            message = int(response[:Packet.length_S_length])
            #Using byte buffer stream to get message
            self.byte_buffer = response[message:]
            if not Packet.corrupt(self.byte_buffer):
                testingPacket = Packet.from_byte_S(response[:message])
                #Check for repeated data
                if testingPacket.seq_num < self.seq_num:
                    print("Repeated Data")
                    t = Packet(response.seq_num, "1")
                    self.network.udt_send(t.get_byte_S())
                #To keep looping until packet is NAK response
                elif testingPacket.msg_S is "1":
                    print("Recieved ACK")
                    self.seq_num += 1
                #When the response packet is NAK response
                elif testingPacket.msg_S is "0":
                    print("RDT 2.1 NAK received")
                    self.byte_buffer = ''
            else:
                print("RDT 2.1 Corrupted ACK")
                self.byte_buffer = ''
        
    def rdt_2_1_receive(self):
        recieveMes = None
        byteSeq = self.network.udt_receive()
        print("byteSeq")
        print(str(byteSeq))
        self.byte_buffer += byteSeq
        print("byte Buffer")
        print(self.byte_buffer)
        currentSeq = self.seq_num
        print("Sequence Number")
        print(currentSeq)
        print("\n")
        while currentSeq == self.seq_num:
            print("Packet Length")
            print(Packet.length_S_length)
            print("Buffer Type")
            print(type(self.byte_buffer))
            print("Buffer Length")
            print(len(self.byte_buffer))
            print("Buffer")
            print(self.byte_buffer)
            #Check if enough bytes have been sent
            if len(self.byte_buffer) < 10:
                break
            #Byte length of message
            lengthB = int(self.byte_buffer[:Packet.length_S_length])
            print("Byte Length")
            print(lengthB)
            print("Byte Buffer Length \n")
            print(len(self.byte_buffer))
            #Check to ensure bytes are of correct length
            if len(self.byte_buffer) < lengthB:
                break
            #Check to see if input packet is corrupt
            if Packet.corrupt(self.byte_buffer):
                print("Packet is corrupt: Sending NAK Message")
                self.network.udt_send(Packet(self.seq_num, "0").get_byte_S)
            #Packet is valid, processing
            else:
                #process buffer segment
                packet = Packet.from_byte_S(self.byte_buffer[0:lengthB])
                #Check if an ACK message
                if packet.msg_S == '1' or '0':
                    #Skip this segment
                    self.byte_buffer = self.byte_buffer[lengthB:]
                    continue
                #Check for if the message contains duplications, if so, send the correction and try again
                elif packet.seq_num < self.seq_num:
                    print("Duplicate ACK message, resend")
                    #Sends ACK
                    self.network.udt_send(Packet(self.seq_num, "1").get_byte_S)
                #Found a valid message to process
                elif packet.seq_num == self.seq_num:
                    print("Valid new message, accept")
                    #Sends ACK
                    self.network.udt_send(Packet(self.seq_num, "1").get_byte_S)
                    #Updates Sequence Number
                    self.seq_num += 1
                #Fill in message
                if recieveMes == None:
                    recieveMes = packet.msg_S
                else:
                    recieveMes = recieveMes + packet.msg_S
            #drop checked packet bytes
            self.byte_buffer = self.byte_buffer[lengthB:]
        #returning Packet
        return recieveMes
        
    def rdt_3_0_send(self, msg_S):
        pass
        
    def rdt_3_0_receive(self):
        pass
        

if __name__ == '__main__':
    parser =  argparse.ArgumentParser(description='RDT implementation.')
    parser.add_argument('role', help='Role is either client or server.', choices=['client', 'server'])
    parser.add_argument('server', help='Server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()
    
    rdt = RDT(args.role, args.server, args.port)
    if args.role == 'client':
        rdt.rdt_2_1_send('MSG_FROM_CLIENT')
        sleep(2)
        print(rdt.rdt_2_1_receive())
        rdt.disconnect()
        
        
    else:
        sleep(1)
        print(rdt.rdt_2_1_receive())
        rdt.rdt_2_1_send('MSG_FROM_SERVER')
        rdt.disconnect()
        


        
        

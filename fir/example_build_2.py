#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from cffi import FFI
ffibuilder = FFI()

srcPath = "/home/xilinx/fir-tests/final/src-hw"
print(os.path.join(srcPath, "cf_stub.c"))

#with open( os.path.join(srcPath, "cpp_FIR.cpp") ) as f:
ffibuilder.set_source("_example",
                      #f.read(),
            r"""
            #include "cf_stub.h"
            
            typedef int data_t;
            typedef int coef_t;
            
            void _p0_cpp_FIR_1_noasync(data_t x[500000], coef_t w[85], data_t ret[500000], data_t datalen);
            void _p0_cpp_FIR_1_noasync(data_t x[500000], coef_t w[85], data_t ret[500000], data_t datalen)
            {
              switch_to_next_partition(0);
              int start_seq[1];
              start_seq[0] = 0;
              cf_request_handle_t _p0_swinst_cpp_FIR_1_cmd;
              cf_send_i(&(_p0_swinst_cpp_FIR_1.cmd_cpp_FIR), start_seq, 1 * sizeof(int), &_p0_swinst_cpp_FIR_1_cmd);
              cf_wait(_p0_swinst_cpp_FIR_1_cmd);
            
            
            #ifdef SDS_DEBUG
              if ((datalen) * 4 != 500000*4)
                printf("x of function cpp_FIR transfer size is different from declared size, system may hang!\n");
              if ((datalen) * 4 != 500000*4)
                printf("ret of function cpp_FIR transfer size is different from declared size, system may hang!\n");
            #endif
            
              cf_send_i(&(_p0_swinst_cpp_FIR_1.x), x, (datalen) * 4, &_p0_request_0);
              cf_send_i(&(_p0_swinst_cpp_FIR_1.w_PORTA), w, 340, &_p0_request_1);
              cf_send_i(&(_p0_swinst_cpp_FIR_1.datalen), &datalen, 4, &_p0_request_3);
            
              cf_receive_i(&(_p0_swinst_cpp_FIR_1.ret), ret, (datalen) * 4, &_p0_cpp_FIR_1_noasync_num_ret, &_p0_request_2);
            
              cf_wait(_p0_request_0);
              cf_wait(_p0_request_1);
              cf_wait(_p0_request_2);
              cf_wait(_p0_request_3);
            }
            """,
            sources=[os.path.join(srcPath, "cf_stub.c"),
                        os.path.join(srcPath, "portinfo.c")],
            include_dirs=["/home/xilinx/fir-tests/final/src-hw/include",
                          "/home/xilinx/fir-tests/final/src-hw"],
            extra_objects=["/usr/lib/libsds_lib.so"])


ffibuilder.cdef("""
    // declarations that are shared between Python and C  
    void _p0_cpp_FIR_1_noasync(int x[500000], int w[85], int ret[500000], 
    int datalen);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

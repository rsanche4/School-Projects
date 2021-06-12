# -*- coding: utf-8 -*-
# Source: https://srome.github.io/Making-A-Markov-Chain-Twitter-Bot-In-Python/
# Edited by: Rafael Sanchez
# June 11, 2021

import tweepy
import time
import numpy as np
import random
import datetime

CONSUMER_KEY = "l3t5n5wPHLfYthmWE84npcNCF"
CONSUMER_SECRET = "kbQ5lni8rNcSs73ND0qPWnhfmDiAo7rM6IV2bYMUxXsrF8Qe54"
ACCESS_KEY = "1378401167588360200-kFaWtgKKZAHLVgtlIYpXAgZ50uG8nf"
ACCESS_SECRET = "up3D6GGRzrnefhEe4lZ93Tje79HtxaDFpSpjxGWngf5TW"

#This initializes everything
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Initial word count, changes with time
WORD_COUNT = 35

# Range of time between tweets in seconds
MIN_TIME = 60
MAX_TIME = 7200

# Corpus extracted from the book "Fundamentals of computer organization and architecture"
corpus = '''
The technological advances witnessed in the computer industry are the result of a
long chain of immense and successful efforts made by two major forces. These
are the academia, represented by university research centers, and the industry,
represented by computer companies. It is, however, fair to say that the current technological advances in the computer industry owe their inception to university
research centers. In order to appreciate the current technological advances in the
computer industry, one has to trace back through the history of computers and
their development. The objective of such historical review is to understand the
factors affecting computing as we know it today and hopefully to forecast the
future of computation. A great majority of the computers of our daily use are
known as general purpose machines. These are machines that are built with no
specific application in mind, but rather are capable of performing computation
needed by a diversity of applications. These machines are to be distinguished
from those built to serve (tailored to) specific applications. The latter are known
as special purpose machines.
Computer systems have conventionally been defined through their interfaces at
a number of layered abstraction levels, each providing functional support to its predecessor. Included among the levels are the application programs, the high-level
languages, and the set of machine instructions. Based on the interface between
different levels of the system, a number of computer architectures can be defined.
The interface between the application programs and a high-level language is
referred to as a language architecture. The instruction set architecture defines the
interface between the basic machine instruction set and the runtime and I/O control.
A different definition of computer architecture is built on four basic viewpoints.
These are the structure, the organization, the implementation, and the performance.
In this definition, the structure defines the interconnection of various hardware components, the organization defines the dynamic interplay and management of the
various components, the implementation defines the detailed design of hardware
components, and the performance specifies the behavior of the computer system.
Computer architects have always been striving to increase the performance of their
architectures. This has taken a number of forms. Among these is the philosophy that
by doing more in a single instruction, one can use a smaller number of instructions to
perform the same job. The immediate consequence of this is the need for fewer
memory read/write operations and an eventual speedup of operations. It was also
argued that increasing the complexity of instructions and the number of addressing
modes has the theoretical advantage of reducing the “semantic gap” between the
instructions in a high-level language and those in the low-level (machine) language.
A single (machine) instruction to convert several binary coded decimal (BCD)
numbers to binary is an example for how complex some instructions were intended
to be. The huge number of addressing modes considered (more than 20 in the
VAX machine) further adds to the complexity of instructions. Machines following
this philosophy have been referred to as complex instructions set computers
(CISCs). Examples of CISC machines include the Intel PentiumTM, the Motorola
MC68000TM, and the IBM & Macintosh PowerPCTM.

Computer technology has shown an unprecedented rate of improvement. This
includes the development of processors and memories. Indeed, it is the advances
in technology that have fueled the computer industry. The integration of numbers
of transistors (a transistor is a controlled on/off switch) into a single chip has
increased from a few hundred to millions. This impressive increase has been
made possible by the advances in the fabrication technology of transistors.
Performance analysis should help answering questions such as how fast can a
program be executed using a given computer? In order to answer such a question,
we need to determine the time taken by a computer to execute a given job. We
define the clock cycle time as the time between two consecutive rising (trailing)
edges of a periodic clock signal. Clock cycles allow counting unit computations,
because the storage of computation results is synchronized with rising (trailing) clock edges.
The time required to execute a job by a computer is often expressed in terms of clock cycles.
While MIPS measures the rate of average instructions, MFLOPS is only defined for
the subset of floating-point instructions. An argument against MFLOPS is the fact
that the set of floating-point operations may not be consistent across machines
and therefore the actual floating-point operations will vary from machine to
machine. Yet another argument is the fact that the performance of a machine for
a given program as measured by MFLOPS cannot be generalized to provide a
single performance metric for that machine.
In order to be able to move a word in and out of the memory, a distinct address
has to be assigned to each word. This address will be used to determine the location
in the memory in which a given word is to be stored. This is called a memory write
operation. Similarly, the address will be used to determine the memory location
from which a word is to be retrieved from the memory. This is called a memory
read operation.
Information involved in any operation performed by the CPU needs to be addressed.
In computer terminology, such information is called the operand. Therefore, any
instruction issued by the processor must carry at least two types of information.
These are the operation to be performed, encoded in what is called the op-code
field, and the address information of the operand on which the operation is to be
performed, encoded in what is called the address field.
Instructions can be classified based on the number of operands as: three-address,
two-address, one-and-half-address, one-address, and zero-address. We explain
these classes together with simple examples in the following paragraphs. It should
be noted that in presenting these examples, we would use the convention operation,
source, destination to express any instruction. In that convention, operation represents the operation to be performed, for example, add, subtract, write, or read.
The source field represents the source operand(s). The source operand can be a constant, a value stored in a register, or a value stored in the memory. The destination
field represents the place where the result of the operation is to be stored, for
example, a register or a memory location.
Control (sequencing) instructions are used to change the sequence in which
instructions are executed. They take the form of conditional branching
(conditional jump), unconditional branching (jump), or call
instructions. A common characteristic among these instructions is that their
execution changes the program counter (PC) value. The change made in the PC
value can be unconditional, for example, in the unconditional branching or the
jump instructions. In this case, the earlier value of the PC is lost and execution of
the program starts at a new value specified by the instruction. Consider, for example,
the instruction jump new-address. Execution of this instruction will cause the
PC to be loaded with the memory location represented by NEW-ADDRESS
whereby the instruction stored at this new address is executed.
The CALL instructions are used to cause execution of the program to transfer to a
subroutine. A call instruction has the same effect as that of the JUMP in terms of
loading the PC with a new value from which the next instruction is to be executed.
However, with the call instruction the incremented value of the PC (to point to the
next instruction in sequence) is pushed onto the stack. Execution of a RETURN
instruction in the subroutine will load the PC with the popped value from the
stack. This has the effect of resuming program execution from the point where
branching to the subroutine has occurred.
Input and output instructions (I/O instructions) are used to transfer data between the
computer and peripheral devices. The two basic I/O instructions used are the INPUT
and OUTPUT instructions. The INPUT instruction is used to transfer data from an
input device to the processor. Examples of input devices include a keyboard or a
mouse. Input devices are interfaced with a computer through dedicated input
ports. Computers can use dedicated addresses to address these ports. Suppose that
the input port through which a keyboard is connected to a computer carries the
unique address 1000. Therefore, execution of the instruction INPUT 1000 will
cause the data stored in a specific register in the interface between the keyboard
and the computer, call it the input data register, to be moved into a specific register
(called the accumulator) in the computer. Similarly, the execution of the instruction
OUTPUT 2000 causes the data stored in the accumulator to be moved to the data
output register in the output device whose address is 2000.
A typical CPU has three major components: (1) register set, (2) arithmetic logic
unit (ALU), and (3) control unit (CU). The register set differs from one computer
architecture to another. It is usually a combination of general-purpose and specialpurpose registers. General-purpose registers are used for any purpose, hence the
name general purpose. Special-purpose registers have specific functions within
the CPU. For example, the program counter (PC) is a special-purpose register
that is used to hold the address of the instruction to be executed next. Another
example of special-purpose registers is the instruction register (IR), which is
used to hold the instruction that is currently executed. The ALU provides the circuitry needed to perform the arithmetic, logical and shift operations demanded of
the instruction set. The control unit is
the entity responsible for fetching the instruction to be executed from the main
memory and decoding and then executing it.
The CPU fetches instructions from memory, reads and writes data from and to
memory, and transfers data from and to input/output devices.
The execution cycle is repeated as long as there are more instructions to execute.
A check for pending interrupts is usually included in the cycle. Examples of interrupts include I/O device request, arithmetic overflow, or a page fault.
When an interrupt request is encountered, a transfer to an interrupt handling routine
takes place. Interrupt handling routines are programs that are invoked to collect the
state of the currently executing program, correct the cause of the interrupt, and
restore the state of the program.
The actions of the CPU during an execution cycle are defined by micro-orders
issued by the control unit. These micro-orders are individual control signals sent
over dedicated control lines. For example, let us assume that we want to execute an
instruction that moves the contents of register X to register Y. Let us also assume
that both registers are connected to the data bus, D. The control unit will issue a control signal to tell register X to place its contents on the data bus D. After some delay,
another control signal will be sent to tell register Y to read from data bus D. The activation of the control signals is determined using either hardwired control or microprogramming.
Registers are essentially extremely fast memory locations within the CPU that are
used to create and store the results of CPU operations and other calculations. Different computers have different register sets.
They differ in the number of registers, register types, and the length of each register. They also differ in the usage of each
register. General-purpose registers can be used for multiple purposes and assigned
to a variety of functions by the programmer. Special-purpose registers are restricted
to only specific functions. In some cases, some registers are used only to hold data
and cannot be used in the calculations of operand addresses. The length of a data
register must be long enough to hold values of most data types. Some machines
allow two contiguous registers to hold double-length values. Address registers
may be dedicated to a particular addressing mode or may be used as address general
purpose. Address registers must be long enough to hold the largest address. The
number of registers in a particular architecture affects the instruction set design.
A very small number of registers may result in an increase in memory references.
Another type of registers is used to hold processor status bits, or flags. These bits
are set by the CPU as the result of the execution of an operation. The status bits
can be tested at a later time as part of another operation.
The CPU is the part of a computer that interprets and carries out the instructions contained in the programs we write. The CPU’s main components are the register file,
ALU, and the control unit. The register file contains general-purpose and special registers. General-purpose registers may be used to hold operands and intermediate results.
The special registers may be used for memory access, sequencing, status information,
or to hold the fetched instruction during decoding and execution. Arithmetic and logical operations are performed in the ALU. Internal to the CPU, data may move from one
register to another or between registers and ALU. Data may also move between the
CPU and external components such as memory and I/O. The control unit is the component that controls the state of the instruction cycle. As long as there are instructions to
execute, the next instruction is fetched from main memory. The instruction is executed
based on the operation specified in the op-code field of the instruction. The control unit
generates signals that control the flow of data within the CPU and between the CPU and
external units such as memory and I/O. The control unit can be implemented using
hardwired or microprogramming techniques.
The assumption of needing no additional time units to recognize branch instructions and computing the target branch address is unrealistic. In typical cases, the
added hardware unit to the fetch unit will require additional time unit(s) to carry
out its task of recognizing branch instructions and computing target branch
addresses. During the extra time units needed by the hardware unit, if other instructions can be executed, then the number of extra time units needed may be reduced
and indeed may be eliminated altogether.
It is interesting to notice that a combination of dynamic and static branch prediction techniques can lead to performance improvement. An attempt to use a dynamic
branch prediction is first made, and if it is not possible, then the system can resort to
the static prediction technique.
In the first arrangement, I/O devices are assigned particular addresses, isolated
from the address space assigned to the memory. The execution of an input instruction at an input device address will cause the character stored in the input register of
that device to be transferred to a specific register in the CPU. In this case, the address and data lines from the CPU can be shared
between the memory and the I/O devices. A separate control line will have to be
used. This is because of the need for executing input and output instructions. In a
typical computer system, there exists more than one input and more than one
output device. Therefore, there is a need to have address decoder circuitry for
device identification. There is also a need for status registers for each input and
output device. The status of an input device, whether it is ready to send data to
the processor, should be stored in the status register of that device.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
I need help. I need help. I need help.
'''

# This is the algorithm for generating the texts
def sample_sentence(corpus, sentence_length, burn_in = 1000):
    corpus = corpus
    sentence = []
    transitions = build_transition_matrix(corpus)
        
    # Make a sentence that is 50 words long
    # We sample the sentence after running through the chain 1000 times to hope
    # to near a stationary distribution.
    current_word = np.random.choice(corpus.split(' '), size=1)[0]
    for k in range(0, burn_in + sentence_length):
        # Sample from the lists with an equal chance for each entry
        # This chooses a word with the correct probability distribution in the transition matrix
        current_word = np.random.choice(transitions[current_word], size=1)[0] 
    
        if k >= burn_in:
            sentence.append(current_word)
            
    return ' '.join(sentence)

def build_transition_matrix(corpus):
    corpus = corpus.split(' ')
    transitions = {}
    for k in range(0,len(corpus)):
        word = corpus[k]
        if k != len(corpus) - 1: # Deal with last word
            next_word = corpus[k+1]
        else:
            next_word = corpus[0] # To loop back to the beginning

        if word not in transitions:
            transitions[word] = []
    
        transitions[word].append(next_word)
    return transitions

# Source: https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

# Posting and also cleaning up a little bit    
while True:
    msg = sample_sentence(corpus, random.randint(2, WORD_COUNT), 10000).replace('\n',' ')
    api.update_status("..." + msg + "...")
    # Range of time randomly chosen between tweets
    sleep_time = random.randint(MIN_TIME, MAX_TIME)
    current_time = datetime.datetime.now()
    print("Latest Status Update: " + str(current_time) + ". Time before next tweet: " + convert(sleep_time))
    time.sleep(sleep_time)

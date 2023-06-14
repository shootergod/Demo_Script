import os

a="""The Segment File Allocator reads entries from the _SCAR from the point of current operation
to the end of the problem solution. The FIAT table entries are created in which attributes of
the data blocks, including their next use (NTU) and last use (LTU), are stored. Data blocks which
are currently assigned to files but are no longer required for problem solution are released.
In certain cases, when the range of use of a data block is large, it may not be possible to
allocate a file to the data block throughout its range of use. In this case, pooling of the
data block is required so that the file to which the data block was assigned may be freed for
another allocation. The next time used (NTU) attribute for a data block is used to efficiently
pool data blocks. In general, the data block whose next use is the furthest from the current
point is pooled, that is, copied onto the Data Pool File (P_L). The format of the Data Pool
File is shown in Figure 5.
One additional check is made with regard to pooling. The operation of the Segment File
Allocator itself is less expensive than a pooling operation. Therefore, pooling occurs only
when the module for which the allocation was required cannot be allocated without pooling.
_hen the Segment File Allocator is complete, a new File Allocation Table (FIAT) has been
generated. This table is used until the solution again reaches a point where a data block is
required to execute an operation but is not assigned to a file.
1.2.3.4 Interpretation of Executive Control Entries (XCEI Sections 4.11, 4.12, 4.13, 4.14)
Executive control entries include the DMAP instructions: REPT, JUMP, C_ND and EXIT.
Executive control entries in the _SCAR are processed by the Executive Control Entry Interpretor
(XCEI). When such an entry is encountered in the _SCAR, the Control Entry Interpretor is called
by XSEMi. If the operation is a jump, cor, ditional jump or repeat, the _SCAR is repositioned
accordingly. If the operation is an exit, the NASTRAN termination routine PEXIT (3.4.22) is
called.
1.2.3.5 Checkpointing Data Blocks (CHKPNT Section 4.10)
The checkpoint module (DNLAP name: CHKPI_T; entry point name: XCHK) copies specified data
blocks required fcr problem restart onto the New Problem Tape and makes appropriate entries
in the restart dictionary. This dictionary is also punched onto cards as each new entry is made.
Thus, in the event of any unscheduled problem interruption, a restart from the last checkpoin"""

# print(a.find('\n'))

print(a.count('\n'))
b = a.replace('\n', ' ')

cmd_str = 'echo ' + b + ' | clip'
os.system(cmd_str)
print(b.count('\n'))
# b = a.split()
print(b)
# CrossDomainGurad and CPU Loading Covert Channels + Client-Server model

Built a Cross-Domain Guard that runs over a QUBES secure operating system ( which runs over a XEN secure hypervisor). The Cross-Domain Guards filters the data that is passed from side to side through it. The CDG process the transferred data through it and filters it , after that it decides if this data is legit and stands by the rules that we have set before. The data was transferred between 2 sides using an application layer protocol that we have also built.
We have modeled a client-server model , to create our environment for the project , The client preforms a financial operations requests using the protocol functions that we have built , and the server process these requests and responds accordingly. ( All of these requests and responds walks through the CDG and gets filtered).
After that , In order to strength the defense mechanism of the CDG, We have tried break the security measures and protocols In the CDG by trying to transfer information from side to side without the CrossDomainGuard Knowledge, In order to do that we have designed and built a CPU-Loading Covert Channel that it's purpose is to bypass the defense mechanisms of the Cross-Domain Guard.

# This ia summary of what i've learnt today on networking foundations

 - what a computer is : a machine that accepts , processes , stores data & prod$
 - CPU  a computer hardware that manages processes in the computer
 - RAM a computer hardware that temporarily stores data during computer process$
 - Storage i.e SSD keeps data permanently
 - NIC connects a computer to a network and it can be etherenet or Wi-Fi
 - hardware and software (physical equipment & programms & instructions that tell hardware what to do 
 - Binary 0s and 1s understood by computers 
 - Bits and bytes 
 - how a web request works : 

1. type in something into my browser i.e google.com using the keyboard 
2. the operating system receives keyboard input and delivers to the browser
3. the browser then creates a network  request  
4. CPU processes instructions from the browserand coordinates with the operating system 
5. RAM then stores active data temporarilywhile it is being processed .
6. NIC converts the requests into signals suitable for my network then send s it out.
7. Router forwards the request to the internet.
8. the internet delivers the request. the request travels through many interconnected networks until it reaches GOOGLRE SERVERS.
9. the servers responds - google servers process the request and sends back the webpage data .
10.the data then returns - response travels back accross the internet , through the my router and into my computer via the NIC 
11.browser displays the webpage - the os passes the data to the browser , which interprates it and displays the webpage on my screen. 



#  MINDSET OF A NETWORK ENGINEER 


1. a network engineer finds out what happens behind the screens or as i term it as behind the GUI . 
 
# Networking Fundamentals – Phase 0

## Networking Mindset & Computer Foundations

### Date Completed

July 2026



# Learning Objectives

By the end of this phase, I was able to:

* Explain what a computer network is.
* Understand why networks exist.
* Describe how computers communicate.
* Differentiate between hardware and software.
* Identify the major components of a computer.
* Understand binary, bits, and bytes.
* Explain how digital information is represented inside a computer.
* Begin thinking like a network engineer by focusing on what happens behind the scenes.



# Core Concepts

## 1. Thinking Like a Network Engineer

A typical computer user focuses on using applications, while a network engineer focuses on understanding what happens behind the scenes 
whenever data is created, processed, transmitted, or received.

A network engineer constantly asks:

> *"What is happening behind the scenes?"*



## 2. What Is a Computer?

A computer performs four basic functions:

1. Receives data (Input)
2. Processes data
3. Stores data
4. Produces output



## 3. Major Computer Components

### CPU (Central Processing Unit)

* Executes instructions.
* Performs calculations.
* Coordinates system operations.
* Often referred to as the "brain" of the computer.

### RAM (Random Access Memory)

* Temporary working memory.
* Stores active programs and data.
* Loses its contents when power is removed.

### Storage (SSD/HDD)

* Permanent storage.
* Stores files, applications, and the operating system.
* Retains information even after shutdown.

### Network Interface Card (NIC)

* Connects the computer to a network.
* Sends and receives network data.
* Can be wired (Ethernet) or wireless (Wi-Fi).



## 4. Hardware vs Software

### Hardware

Physical components of a computer.

Examples:

* CPU
* RAM
* SSD
* Keyboard
* Mouse
* Network Interface Card

### Software

Programs that instruct the hardware.

Examples:

* macOS
* Python
* Google Chrome
* VS Code



## 5. Computer Networks

A computer network is a collection of connected devices that communicate and share resources.

Networks allow devices to share:

* Files
* Internet access
* Printers
* Applications
* Other computing resources



## 6. Binary

Computers only understand binary.

Binary consists of two values:

* 0
* 1

A transistor can only be ON or OFF, making binary the natural language of computer hardware.



## 7. Bits and Bytes

* 1 bit = one binary digit
* 8 bits = 1 byte
* 1 KB = 1,024 bytes
* 1 MB = 1,024 KB
* 1 GB = 1,024 MB
* 1 TB = 1,024 GB


## 8. Digital Data

Everything inside a computer is represented as binary.

Examples include:

* Text
* Images
* Audio
* Video
* Programs


# Key Takeaways

* Computers process everything using binary.
* RAM stores temporary data, while storage keeps data permanently.
* The CPU executes instructions.
* The NIC enables network communication.
* Every network request passes through several hardware and software components before reaching its destination.
* Understanding what happens behind the scenes is the foundation of networking.


# Personal Insights & Real-World Connections

## CPU vs Python's `main.py`

While learning networking, I wondered whether the CPU was equivalent to `main.py` in a Python project.

I learned that `main.py` is simply the starting point of a program. The CPU is physical hardware responsible for executing machine 
instructions. Between them sits the Python interpreter, which translates Python code into instructions that the CPU can execute.



## File Storage vs RAM

During my Task Tracker System project, my `tasks.txt` file kept being overwritten whenever the CLI restarted.

Initially, I suspected RAM might be responsible because the data appeared to disappear.

I learned that text files are stored on permanent storage, not RAM. The issue was caused by my program's file-writing logic rather than 
computer memory or Git.



## Mobile Data, Ethernet, Wi-Fi, and NICs

I learned that:

* Mobile data uses a cellular network.
* Wi-Fi is a wireless local networking technology.
* Ethernet is a wired networking technology.
* An Ethernet cable is not a Network Interface Card (NIC); the NIC is the hardware that sends and receives data, while the cable carries 
the signals.


## Website Connectivity

While accessing the iTax portal, I experienced "Website cannot be reached" and "Session timed out" errors.

I learned that these issues can involve multiple networking concepts such as Internet connectivity, DNS, servers, browser caching, or HTTP 
sessions. I will revisit this example after learning those topics.



## RAM vs Permanent Storage

RAM is much faster because it is designed to provide the CPU with rapid access to active data. Permanent storage is optimized for 
retaining information after power is removed rather than maximizing access speed.



# Future Questions

Topics that will be answered in later phases:

* How does Ethernet actually transmit data?
* How do switches forward data?
* How do routers know where to send information?
* How does Wi-Fi work internally?
* How does DNS locate websites?
* How are IP addresses assigned?
* How does the Internet route data between countries?



# Phase Reflection

This phase changed the way I think about computers. I no longer see a computer as simply a machine that runs applications. I now 
understand the individual responsibilities of the CPU, RAM, storage, the operating system, and the Network Interface Card.

One of my biggest takeaways is that computers do not understand words, images, or videos directly. Everything is ultimately represented as 
binary and processed through layers of software before being executed by the hardware.

I also found it valuable to connect networking concepts with my previous Python projects, Git experience, and real-world situations such 
as troubleshooting website connectivity. These connections helped reinforce my understanding and showed me how networking concepts apply 
outside the classroom.


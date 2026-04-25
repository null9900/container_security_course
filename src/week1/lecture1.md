# What is a container?

|||objectives
After this lecture, you should be able to answer the following:
- What is this course all about?
- What are containers and why are they important?
- What are the uses of containers?
|||

You have a powerful computer, 64 cores, 128 GB of RAM. You think: why not rent some of this power and make money?

Some want to host websites, others want to run simulations, others need background services. Business is doing great!
Then the chaos starts. One app eats all the RAM and crashes everyone else. Someone installs a sketchy library that breaks three other services. Another one updates their database and takes down half the machine.

You need boundaries. Each person's software should be isolated so they can't see or break each other's stuff. You also need to control how much CPU and memory each one gets. 

**How do you do that?**

![Containers-before-after](./week1/container_after_before.png)

### Why not Virtual Machines?

* Lightweight
* Fast startup
* Portability

<div style="display: flex; gap: 10px; justify-content: center;">
  <img src="./week1/old_containers.jpg" style="width: 33%;" />
  <img src="./week1/old_containers2.jpg" style="width: 33%;" />
  <img src="./week1/new_containers.jpg" style="width: 33%;" />
</div>


The main difference between virtual machines and containers is **kernel sharing**.

![Containers-old](./week1/container_vs_vm.png)

### Why is learning about containers important?
* Because they are everywhere.
* Knowing how the containers work will be useful in your career. 

### Why focus on Docker?

Docker is the most popular container solution. 

Docker processes **13 billion** container downloads every month.

### How are we going to study this course?

* 1 recorded lecture per week.
* 1 optional live session every two weeks for Q/A.
* The course will focus on the practical and application aspects rather than pure theory.

### What do you need to study this course?

* Basic understanding of Operating Systems.
* Basic understanding of Linux commands.
* Having a Linux VM installed.

|||quiz
- What is a container? 
- What are the uses of containers?
- What is the difference between a virtual machine and a container?
- Make sure to have a Linux VM installed and ready for the next lectures.
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>

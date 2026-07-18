# Namespaces and Chroot

|||objectives
After this lecture, you should be able to answer the following:
- What is a namespace, and what do UTS, PID, and NET namespaces isolate?
- What does chroot do?
- How do these combine into a container?
|||

A container is just a normal process built from a few ordinary Linux kernel features. In this lecture, we will build one (sort of) by hand.

### What is a Namespace?

A namespace is a kernel feature that gives a process its own private view of some part of the system. Two processes in different namespaces can look at the same kind of resource and see completely different things.

### UTS Namespace (hostname)

The UTS namespace isolates the hostname.

```bash
sudo unshare --uts sh
hostname mycontainer
hostname
```

### PID Namespace (process IDs)

The PID namespace isolates the process tree. A process in a new PID namespace gets its own numbering starting from PID 1 and cannot see processes outside.

```bash
sudo unshare --pid --fork --mount-proc sh
ps aux
```

### NET Namespace (network)

The NET namespace isolates the network stack: interfaces, IP addresses, routing, and ports.

```bash
sudo unshare --net sh
ip addr
```

### Combining Namespaces

A real container uses several namespaces at once. You can combine them:

```bash
sudo unshare --uts --pid --net --fork --mount-proc sh
```

This shell now has its own hostname, process tree, and network.

### chroot: Isolating the Filesystem

`chroot` changes what a process sees as the root directory (`/`). After `chroot`, the process is trapped inside a directory and cannot see anything above it.


```
# Download alpine filesystem from here
https://alpinelinux.org/downloads/
```
You now have a full Alpine filesystem (`bin`, `etc`, `lib`, and so on). Chroot into it:

```bash
sudo chroot alpine-root /bin/sh
ls /
```

Inside, `/` is now the Alpine filesystem, not the host's. The process cannot see the host's files at all. Combined with namespaces, our process now has its own hostname, processes, network, and filesystem.

|||warning
Chroot is not a security boundary. It only changes what a process sees as /. It does not isolate users, processes, or capabilities, and there are well-known ways for a privileged process to escape a chroot "jail". Real containers do not rely on chroot alone. Docker uses pivot_root inside a dedicated mount namespace, which lets it detach the old root filesystem entirely so the container cannot reach back to it. We use chroot here because it is simple and shows the idea.
|||

### So What Does Docker Actually Do?

When you type `docker run`, Docker:

1. Pulls and unpacks the image's layers into a root filesystem (the chroot target).
2. Creates a set of namespaces for isolation.
3. Configures networking (virtual ethernet pair, bridge, port mapping).
4. Runs your command as PID 1 inside all of that.

Everything you learned in this course, the layers, the isolation, the networking, comes back to these kernel primitives. Docker is a convenient wrapper around features the Linux kernel already provides.

### The Big Picture

A container feels like a lightweight virtual machine, but it is something quite different. There is no second operating system and no virtual hardware. There is a normal process on your host, wrapped in namespaces so it sees only its own world, and chrooted into its own filesystem. Once you see it this way, it becomes clear that once you break any of these boundaries, the container is just a process on your machine again.

|||quiz
- What is a namespace, in your own words?
- What does each of the UTS, PID, and NET namespaces isolate?
- What does `chroot` add that namespaces alone do not?
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>
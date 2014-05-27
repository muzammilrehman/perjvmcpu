perjvm cpu
================

python lib to collect the all java process running currently only supported Linux IS on a system and then monitor its cpu 
usage. I wrote the class when I could not fine a easy to use solution and interfacing with java was very difficult.

###Requirements
1. psutil
2. collections
3. logger


##Example
class _requires_ the java name pattern like "-Dprogram.name="

1. Compile the java code 

 `javac HelloWorld.java`

2. Start the java process

 `java -Dprogram.name="HelloWorld" HelloWorld`


   
#### Java example code
    public class HelloWorld { 
     public static void main(String[] args) { 
      while(true)
      {
        try {
            Thread.sleep(1000L);
            String foo = "123213 * 1312312313 * 123123123 * 12312 / 123123123123 % 123123 * 234234820394809234 + 123123213123";
            System.out.println("Hello, World");
            } 
        catch(InterruptedException ex) 
            {
            Thread.currentThread().interrupt();
            }
      }
     }
    }
    


#### python 
    import PerJvmCpu
    ob = PerJvmCpu.PerJvmCpu(name_pattern="-Dprogram.name=", interval=10, exclude_list=['-Didea.paths.selector=PyCharm30'])
    for pid in ob.get_pid_details():
       print ob.cpu_stats(pid)



###Once you have the cpu and java process name you can do anything like send them to graphing lib to plot the cpu utilization 



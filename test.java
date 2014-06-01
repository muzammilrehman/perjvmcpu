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

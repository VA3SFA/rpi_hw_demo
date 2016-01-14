/*
 * Code found from http://wiringpi.com/examples/blink/
 */
#include <wiringPi.h>
int main (void)
{
  wiringPiSetup () ;
  pinMode (18, OUTPUT) ;
  for (;;)
  {
    digitalWrite (18, HIGH) ; delay (500) ;
    digitalWrite (18,  LOW) ; delay (500) ;
  }
  return 0 ;
}

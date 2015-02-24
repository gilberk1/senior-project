#include <m8c.h>        // part specific constants and macros
#include "PSoCAPI.h"    // PSoC API definitions for all User Modules
#include "psocdynamic.h"	// PSoC API definitions for Dynamic Recongiguration
#include <stdio.h>
#include <string.h>

#pragma interrupt_handler RX8ISR

typedef
enum
{
	PARSE_STATE_INIT,
	PARSE_STATE_WIFI,
	PARSE_STATE_LAT,
	PARSE_STATE_LONG
} states;

int rptr = 0;
int wptr = 0;
int str_ptr;
char serbuf[128];
char wifi_str[32];
char lat[32];
char lon[32];
char tempchar;
long count=0;
states state = PARSE_STATE_INIT;

char debugstring[32];

void main(void)
{	
    // Enable Global Interrupts
    M8C_EnableGInt;      
   
    // Start baud rate generator
    Counter8_1_Start();       
   
    LCD_1_Start();
	
    // Load the receiver configuration
    LoadConfig_Receiver();
	
	RX8_2_Start(RX8_2_PARITY_NONE);
	
	RX8_2_EnableInt();
	
	while (1)
	{
		LCD_1_Position(1,0);
		csprintf(debugstring,"%d %d",rptr,wptr);
		LCD_1_PrString(debugstring);
		// check for new char
		++count;
		LCD_1_Position(1,8);
		if ((count >> 12) & 1)
		{
			LCD_1_PrCString("*");
		}
		else
		{
			LCD_1_PrCString("_");
		}
		while (rptr != wptr)
		{
			// new char
			char newchar;
			newchar = serbuf[rptr];
			rptr++;
			if (rptr == 128)
			{
				rptr = 0;
			}
			if (newchar == ';')
			{
				state = PARSE_STATE_WIFI;
				str_ptr = 0;
			}
			else
			{
				switch (state)
				{
					case (PARSE_STATE_WIFI):
						if (newchar == ':')
						{
							state = PARSE_STATE_LAT;
							str_ptr = 0;
						}
						else
						{
							wifi_str[str_ptr++] = newchar;
							LCD_1_Position(0,0);
							LCD_1_PrString(wifi_str);
						}
						break;
					case (PARSE_STATE_LAT):
						if (newchar == '!')
						{
							state = PARSE_STATE_LONG;
							str_ptr = 0;
						}
						else
						{
							lat[str_ptr++] = newchar;
							LCD_1_Position(0,4);
							LCD_1_PrString(wifi_str);
						}
						break;
					case (PARSE_STATE_LONG):
						if (newchar == '#')
						{
							state = PARSE_STATE_INIT;
							str_ptr = 0;
						}
						else
						{
							lon[str_ptr++] = newchar;
						}
						break;
				}
			}
		}
	}
}
	
void RX8ISR(void)
{
	serbuf[wptr++] = tempchar;   // Put the new char into our ring buffer, advance write ptr
	
	tempchar = RX8_2_cReadChar();  // Use the data access method, or read the register directly
 
	if (wptr == 128)   // Check to see if we need to wrap wptr
		{              
         	wptr = 0;
        } 	
	return;
}

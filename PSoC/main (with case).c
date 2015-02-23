#include <m8c.h>        // part specific constants and macros
#include "PSoCAPI.h"    // PSoC API definitions for all User Modules
#include "psocdynamic.h"	// PSoC API definitions for Dynamic Recongiguration
#include <stdio.h>
#include <string.h>

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
	
	while (1)
	{	
	typedef
		enum
		{
			PARSE_STATE_INIT,
			PARSE_STATE_WIFI,
			PARSE_STATE_LAT,
			PARSE_STATE_LONG
		} states;

	int str_ptr;
	char wifi_str[32];
	char lat[32];
	char lon[32];
	char newchar;
	
	states state = PARSE_STATE_INIT;
		// new char
		newchar = RX8_2_cGetChar();
		
		switch (state)
		{
			case (PARSE_STATE_INIT):
				if (newchar == ';')
				{
					state = PARSE_STATE_WIFI;
					str_ptr = 0;
				}
				break;
			
			case (PARSE_STATE_WIFI):
				while(newchar != ':')
				{
					wifi_str[str_ptr++] = newchar;
				}
				state = PARSE_STATE_LAT;
				LCD_1_Position(0,0);
				LCD_1_PrString(wifi_str);
				str_ptr = 0;
				break;
				
			case (PARSE_STATE_LAT):
				while(newchar != '!')
				{
					lat[str_ptr++] = newchar;
				}
				state = PARSE_STATE_LONG;
				LCD_1_Position(0,7);
				LCD_1_PrString(lat);
				str_ptr = 0;
				break;
				
			case (PARSE_STATE_LONG):
				while(newchar != '#')
				{
					lon[str_ptr++] = newchar;
				}
				state = PARSE_STATE_INIT;
				LCD_1_Position(1,7);
				LCD_1_PrString(lon);
				str_ptr = 0;
				break;
		}
		
	}
}


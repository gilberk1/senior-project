//--------------------------------------------------------------------------
//
// Copyright 2013, Cypress Semiconductor Corporation.
//
// This software is owned by Cypress Semiconductor Corporation (Cypress)
// and is protected by and subject to worldwide patent protection (United
// States and foreign), United States copyright laws and international
// treaty provisions. Cypress hereby grants to licensee a personal,
// non-exclusive, non-transferable license to copy, use, modify, create
// derivative works of, and compile the Cypress Source Code and derivative
// works for the sole purpose of creating custom software in support of
// licensee product to be used only in conjunction with a Cypress integrated
// circuit as specified in the applicable agreement. Any reproduction,
// modification, translation, compilation, or representation of this
// software except as specified above is prohibited without the express
// written permission of Cypress.
//
// Disclaimer: CYPRESS MAKES NO WARRANTY OF ANY KIND,EXPRESS OR IMPLIED,
// WITH REGARD TO THIS MATERIAL, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
// Cypress reserves the right to make changes without further notice to the
// materials described herein. Cypress does not assume any liability arising
// out of the application or use of any product or circuit described herein.
// Cypress does not authorize its products for use as critical components in
// life-support systems where a malfunction or failure may reasonably be
// expected to result in significant injury to the user. The inclusion of
// Cypress' product in a life-support systems application implies that the
// manufacturer assumes all risk of such use and in doing so indemnifies
// Cypress against all charges.
//
// Use may be limited by and subject to the applicable Cypress software
// license agreement.
//
//--------------------------------------------------------------------------
//*****************************************************************************
//*****************************************************************************
//  FILENAME: main.c
//   Version: 1.1, Updated on 04 Aril 2013
//
//  DESCRIPTION: Main file of the HalfDuplexUART Project.
//
//-----------------------------------------------------------------------------
//  Copyright (c) Cypress MicroSystems 2009-2013. All Rights Reserved.
//*****************************************************************************
//*****************************************************************************
//***************************************************************************************
//
//    The project can be tested using Windows HyperTerminal application.
// 
//    CY3210-PSoCEVAL1 Board Project
//
//Project Objective
//    To demonstrate the operation of the 8-Bit Half Duplex UART using Dynamic Reconfiguration.  
//
//Overview
//    A character is  transmitted by a Personal Computer using Windows Hyper Terminal,
//     through a Serial Port. The data is received and echoed back to the PC.
//
//
//    The following changes were made to the default settings in the Device Editor:
// 
//    Selection and Placement of User Modules
//        o Select a Counter8_1 User Module and place it as it is in the base configuration.
//          Place this module in the digital block DBB01
//        o Add a new loadable configuration in the project and remane it as 'Receiver'. 
//           Select a RX8_1 User Module and place it in this configuration in the digital 
//		   communication block DCB02.
//     	  o Add a new loadable configuration in the project and remane it as 'Transmitter'. 
//           Select a TX8_1 User Module and place it in this configuration in the digital 
//		   communication block DCB02.
//
//    Set the global resources and UM parameters in the Device Editor as shown under 
//    "Project Settings" ahead.
//
//    Upon program execution all hardware settings from the device configuration are loaded 
//    into the device and main.c is executed.
//
//    The 24 MHz system clock is divided by 1(VC1)is provided to Counter8_1 user module.
//    The period of this 8 bit counter is set as 155 and the Compare Value is set as 78.
//    This gives an output with frequency 153.864Kbps. This is 8 times the baud rate 
//    of the half duplex UART ie. 19200 bps.
//    
//    This counter is started in firmware. This is followed by loading the Receiver 
//    configuration which starts the RX8_1 module. Once the PSoC receives a character from the 
//    PC, it comes out of the receiver mode and loads the Transmitter configuration. The 
//    TX8_1 module is started in this configuration. The PSoC echos back the received character
//    to the PV with a couple of carriage return and line feed commands.
//
//    Further information on user modules is supplied in the specific user module data sheet 
//    included with PSoC Designer.
//
//Clock Routing
//    None
//
//Project Settings
//
//    Global Resources 
//        CPU_Clock      = SysClk/2          CPU clock set to 12 MHz
//
//User Module Parameters
//
//1.  Counter8_1
//
//     Clock			VC1						VC1 = 24MHz
//     ClockSync		Use SysClock Direct		Since the clock to the UM is fed directly from 
//												the SysClock, it must be synchronized with the 
//												SysClock  directly to comply with the Nyquist 
//												Criterion. 
//     Enable			High					The Enable input of the UM is tied to HIGH logic.
//     CompareOut		None					The CompareOut output is not used in this 
//												application.
//     TerminalCountOut	None					The TerminalCountOut is not used in this 
//												application.
//     Period			155						The divider of the counter is set to 156 (Period + 1)
//     CompareValue		78						This parameter sets the Duty Cycle of the Counter to 50%
//	   CompareType		Less Than or Equal To	This value sets the Counter divider to (Period + 1)
// 	   InterruptType	Terminal Count			Default.  Interrupt is not used in the project
//	   InvertEnable		Normal					The Enable input to Counter is active-high
//
//2.   RX8_1
//
//	    Clock			DBB01					The clock is derived from Counter8_1
//	    Input			Row_0_Input_2			Port pin P1.6 has been assigned as the input for
//												the half duplex UART. The input from this pin to
//												the RX8_1 block is routed via the Row_0_Input_1 net.
//	    ClockSync		Sync To SysClock		Clock is synchronized with the SysClock.
//      RxCmdBuffer		Disable					Buffer for Command Processing is disabled.
//	    RxBufferSize	16 Bytes				Not applicable as the RxCmdBuffer is disabled.
//	    RX Output		None					Rx data Output is not used
//	    Data Clock Out	None					Rx Clock output is not used
//		InvertInput		Normal					The input signal is not inverted. 
//
//3.    TX8_1
//
//		Clock				DBB01				The clock is derived from Counter8_1
//		Output				Row_0_Output_3		Port pin P2.7 has been assigned as the output 
//												for the half duplex UART. The output from the 
//												TX8_1 block is routed to this pin via the 
//												Row_0_Output_3 net.
//		TX  Interrupt Mode	TxRegEmpty			Default value.  Interrupt is not used in this project
//		ClockSync			Sync to SysClock	Clock is synchronized with SysClock.
//		Data Clock Out		None	

// Note : For more information on the User module parameters and their API, refer the User module data
//		  sheets
//
// Hardware Connections
//
// Input
//    Pin	    Select	            Drive
//    -----------------------------------------
//    P1[6]	GlobalInOdd_6	        High Z
//			
// Output
//
//    Pin	    Select	            Drive
//    -----------------------------------------
//    P2[7]	GlobalOutEven_7	        Strong
//
// Using the CY3210 Evaluation Board
//        � Connect a jumper wire between P1[6] and Rx of J13.
//        � Connect a jumper wire between P2[7] and Tx of J13.
//
//How to use Hyperterminal of Windows
//    � Connect a 9 pin Male to Female (one to one RS232) Serial cable from PC's  serial port 
//      cto EVAL board serial port.
//
//    � Setting up HyperTerminal in Windows.
//
//	Click Start -> Program Files -> Accessories -> Communication -> HyperTerminal
//
//    	- Enter a Name and select OK.
//    
//    	- In ConnectTo option
//        
//        - Select the 'Connect using' as COM1/COM2 in which the serial cable is connected 
//          and Click OK
//
//    	- In the COM1 properties
//    		- Bits per second 	= 19200
//    		- Data bits		    = 8
//    		- Parity			= None
//    		- Stop Bits		    = 1
//    		- Flow Control		= None
//
//		    click OK
//
//        - Further, click on File-Properties-Settings-Ascii Setup and
//           Enable "Echo typed characters locally" (The HyperTerminal should
//           in Disconnected mode while setting this option) 
//
//    Note: The Hyper Terminal should be in Connected mode before Running PSoC.
//
//-----------------------------------------------------------------------------
//  Include Files
//-----------------------------------------------------------------------------
#include <m8c.h>        // part specific constants and macros
#include "PSoCAPI.h"    // PSoC API definitions for all User Modules
#include "psocdynamic.h"	// PSoC API definitions for Dynamic Recongiguration

char InputChar;

void main(void)
{
   int buf_widx = 0;	// Initialize the write index at the beginning of time
   
   // Enable Global Interrupts
   M8C_EnableGInt;      
   
   // Start baud rate generator
   Counter8_1_Start();       
   
   LCD_1_Start();
	
   // Load the receiver configuration
   LoadConfig_Receiver();
	
   while(1)
   {
	  char string_buf[17];
	  int lin_idx;
	
	  string_buf[16] = '\0';    // Stuff a NULL character at the end of the string buffer, for safety    
	  
      // Start RX8
      RX8_2_Start(RX8_2_PARITY_NONE); 
	  
	    LCD_1_Position(0,0);
		LCD_1_PrCString("s");
	
      // Wait for character.
      InputChar = RX8_2_cGetChar();   

	  
	  // If the new char = 0x2 or 0x3 (start of string), then reset write index = 0, 
	  // save the current line into lin_idx, and continue
	  // Else if the new char != 0x4 then store new char at current write index, increment write index
	  //     and do error checking to make sure that write index is in bounds
	  // Else (new char == 0x4) then send the string to the LCD display, making sure to erase any training
	  //    LCD display slots that have been updated, 16 - strlen(message).
	
	LCD_1_Position(0,buf_widx);
	buf_widx = (buf_widx + 1) & 0xF;
	string_buf[0] = InputChar;
	string_buf[1] = '\0';
	LCD_1_PrString(string_buf);
	
	  // Stop the RX8_1 UM
	  //RX8_1_Stop(); 
	   
      // Unload the receiver configuration
      //UnloadConfig_Receiver();

   }
}


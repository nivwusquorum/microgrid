#ifndef COMMUNICATION_MESSAGES_H
#define COMMUNICATION_MESSAGES_H

#include "shared/communication/message.h"

typedef enum {
    UMSG_PING = 0,
    UMSG_GET_TIME = 1,
    UMSG_SET_TIME = 2,
    UMSG_CRON_STATS = 3,
    // leave last (also make sure no gaps above)
    UMSG_TOTAL_MESSAGES 
} MessageToUlink; 

typedef enum {
    CMSG_DEBUG = 0,
    CMSG_GET_TIME_REPLY = 1,
    // leave last (also make sure no gaps above)
    CMSG_TOTAL_MESSAGES
} MessageToComputer;

void handle_message(Message*);

void set_message_handler(MessageToUlink msg_type,
                          void (*handler)(Message*));

void register_misc_message_handlers();

#endif
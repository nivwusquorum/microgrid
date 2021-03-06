#ifndef DEMAND_RESPONSE_COMMON_H
#define DEMAND_RESPONSE_COMMON_H

typedef enum {
    DR_STATE_GREEN = 0,
    DR_STATE_YELLOW = 1,
    DR_STATE_RED = 2,
    DR_STATE_OFF = 3,
    DR_STATE_ON = 4,
            
    DR_STATE_TOTAL
} DemandResponeState;

const char* dr_state_as_string(DemandResponeState state);

int state_to_price_coefficient(DemandResponeState state);

#endif
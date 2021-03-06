/* 
 * File:   MessageBuilder.h
 * Author: sidor
 *
 * Created on January 22, 2015, 1:24 AM
 */

#ifndef SHARED_COMMUNICATION_UTILS_MESSAGEBUILDER_H
#define	SHARED_COMMUNICATION_UTILS_MESSAGEBUILDER_H

#include <stdarg.h>
#include <stdint.h>

typedef struct StructMessageBuilder {
    int next_char;
    int capacity;
    char* message;
} MessageBuilder;

// Creates new message wrapper and allocates buffer memory.
void make_mb(MessageBuilder* mb, int initial_capacity);

// Makes a copy of mb. If deep is 1 it copies internal buffer as well.
MessageBuilder* mb_copy(MessageBuilder* mb, int deep);

// Takes strlen(str) bytes.
void mb_add_string(MessageBuilder* mb, const char* str);

// Uses 1 byte
void mb_add_char(MessageBuilder* mb, char chr);

// Uses four bytes.
void mb_add_int(MessageBuilder* mb, int d);

// Uses two bytes
void mb_add_int_noprefix(MessageBuilder* mb, int d);

// Uses six bytes.
void mb_add_float(MessageBuilder* mb, float f);

// Uses four bytes
void mb_add_float_noprefix(MessageBuilder* mb, float f);

// Uses six bytes
void mb_add_uint32(MessageBuilder* mb, uint32_t ld);

// Uses four bytes.
void mb_add_uint32_noprefix(MessageBuilder* mb, uint32_t ld);

// Accepts print like syntax
void mb_add_formated(MessageBuilder* mb, const char* format, ...);

// Accepts already initiated arguments - useful for wrapping
// build function.- 
void mb_add_formated_args(MessageBuilder* mb, const char* format, va_list args);

#endif	/* MESSAGEBUILDER_H */


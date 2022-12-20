/*
 * This file is part of the MicroPython for Monocle:
 *      https://github.com/Itsbrilliantlabs/monocle-micropython
 *
 * Authored by: Josuah Demangeon <me@josuah.net>
 *
 * ISC Licence
 *
 * Copyright © 2022 Brilliant Labs Inc.
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
 * REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
 * AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
 * INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
 * LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
 * OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
 * PERFORMANCE OF THIS SOFTWARE.
 */

#include <stddef.h>

#include "py/obj.h"
#include "py/objarray.h"
#include "py/runtime.h"

#include "nrfx_log.h"

#include "driver_fpga.h"
#include "driver_spi.h"
#include "driver_config.h"
#include "machine.h"

STATIC mp_obj_t machine_camera_capture(void)
{
    fpga_camera_capture();
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(machine_camera_capture_obj, &machine_camera_capture);

STATIC const mp_rom_map_elem_t machine_camera_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_capture),     MP_ROM_PTR(&machine_camera_capture_obj) },
};
STATIC MP_DEFINE_CONST_DICT(machine_camera_locals_dict, machine_camera_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    machine_camera_type,
    MP_QSTR_Camera,
    MP_TYPE_FLAG_NONE,
    locals_dict, &machine_camera_locals_dict
);

<?php

namespace Database\Seeders;

use App\Modules\Lop\Models\Lop;
use Illuminate\Database\Seeder;

class LopSeeder extends Seeder
{
    public function run(): void
    {
        $lops = [
            ['MaLop' => 'CNTT-K63A', 'TenLop' => 'CNTT K63 A', 'MaNganh' => 'CNTT'],
            ['MaLop' => 'CNTT-K63B', 'TenLop' => 'CNTT K63 B', 'MaNganh' => 'CNTT'],
            ['MaLop' => 'KHMT-K63A', 'TenLop' => 'KHMT K63 A', 'MaNganh' => 'KHMT'],
            ['MaLop' => 'MKT-K63A',  'TenLop' => 'Marketing K63 A', 'MaNganh' => 'MKT'],
            ['MaLop' => 'QTKD-K63A', 'TenLop' => 'QTKD K63 A', 'MaNganh' => 'QTKD'],
            ['MaLop' => 'TA-K63A',   'TenLop' => 'Tiếng Anh K63 A', 'MaNganh' => 'TA'],
            ['MaLop' => 'DLKS-K63A', 'TenLop' => 'DLKS K63 A', 'MaNganh' => 'DLKS'],
        ];

        foreach ($lops as $lop) {
            Lop::updateOrCreate(['MaLop' => $lop['MaLop']], $lop);
        }
    }
}

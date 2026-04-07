<?php

namespace Database\Seeders;

use App\Modules\Nganh\Models\Nganh;
use Illuminate\Database\Seeder;

class NganhSeeder extends Seeder
{
    public function run(): void
    {
        $nganhs = [
            ['MaNganh' => 'CNTT', 'TenNganh' => 'Công nghệ thông tin', 'MaKhoa' => 'CN'],
            ['MaNganh' => 'KHMT', 'TenNganh' => 'Khoa học máy tính', 'MaKhoa' => 'CN'],
            ['MaNganh' => 'KTPM', 'TenNganh' => 'Kỹ thuật phần mềm', 'MaKhoa' => 'CN'],
            ['MaNganh' => 'MKT',  'TenNganh' => 'Marketing', 'MaKhoa' => 'KT'],
            ['MaNganh' => 'QTKD', 'TenNganh' => 'Quản trị kinh doanh', 'MaKhoa' => 'KT'],
            ['MaNganh' => 'TA',   'TenNganh' => 'Tiếng Anh', 'MaKhoa' => 'NN'],
            ['MaNganh' => 'DLKS', 'TenNganh' => 'Du lịch và Khách sạn', 'MaKhoa' => 'DL'],
        ];

        foreach ($nganhs as $nganh) {
            Nganh::updateOrCreate(['MaNganh' => $nganh['MaNganh']], $nganh);
        }
    }
}

<?php

namespace App\Modules\SinhVien\Services;

use App\Modules\SinhVien\Models\SinhVien;

class SinhVienService
{
    public static string $model = SinhVien::class;

    public function all(array $columns = ['*'])
    {
        return SinhVien::with(['lop.nghanh.khoa'])->get($columns);
    }

    public function find(string $maSV)
    {
        return SinhVien::with(['lop.nghanh.khoa', 'hsoXetTuyen'])->find($maSV);
    }

    public function create(array $data): SinhVien
    {
        return SinhVien::create($data);
    }

    public function update(string $maSV, array $data): bool
    {
        return SinhVien::find($maSV)?->update($data);
    }

    public function delete(string $maSV): bool
    {
        return SinhVien::find($maSV)?->delete();
    }

    public function paginate(int $perPage = 15)
    {
        return SinhVien::with(['lop.nghanh.khoa'])->paginate($perPage);
    }

    public function search(string $keyword)
    {
        return SinhVien::with(['lop.nghanh.khoa'])
            ->where('HoTen', 'like', "%{$keyword}%")
            ->orWhere('MaSV', 'like', "%{$keyword}%")
            ->orWhere('Email', 'like', "%{$keyword}%")
            ->get();
    }
}

<?php

namespace App\Modules\Khoa\Services;

use App\Modules\Khoa\Models\Khoa;

class KhoaService
{
    public static string $model = Khoa::class;

    public function all()
    {
        return Khoa::with('nganhs')->get();
    }

    public function find(string $maKhoa)
    {
        return Khoa::with('nganhs')->find($maKhoa);
    }

    public function create(array $data): Khoa
    {
        return Khoa::create($data);
    }

    public function update(string $maKhoa, array $data): bool
    {
        return Khoa::find($maKhoa)?->update($data);
    }

    public function delete(string $maKhoa): bool
    {
        return Khoa::find($maKhoa)?->delete();
    }

    public function paginate(int $perPage = 15)
    {
        return Khoa::with('nganhs')->paginate($perPage);
    }
}

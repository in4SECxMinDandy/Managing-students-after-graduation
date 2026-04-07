<?php

namespace App\Modules\Khoa\Http\Livewire;

use App\Modules\Khoa\Models\Khoa;
use App\Modules\Khoa\Services\KhoaService;
use Livewire\Component;

class KhoaCreate extends Component
{
    public string $maKhoa = '';
    public string $tenKhoa = '';

    protected array $rules = [
        'maKhoa' => 'required|string|size:2|unique:khoa,MaKhoa',
        'tenKhoa' => 'required|string|max:100|unique:khoa,TenKhoa',
    ];

    protected array $messages = [
        'maKhoa.required' => 'Mã khoa là bắt buộc.',
        'maKhoa.size' => 'Mã khoa phải có đúng 2 ký tự.',
        'maKhoa.unique' => 'Mã khoa đã tồn tại.',
        'tenKhoa.required' => 'Tên khoa là bắt buộc.',
        'tenKhoa.unique' => 'Tên khoa đã tồn tại.',
    ];

    public function save(KhoaService $service)
    {
        $this->validate();
        $service->create(['MaKhoa' => $this->maKhoa, 'TenKhoa' => $this->tenKhoa]);
        session()->flash('success', 'Thêm khoa thành công!');
        $this->reset(['maKhoa', 'tenKhoa']);
    }

    public function render()
    {
        return view('livewire.khoa.create')
            ->extends('layouts.app')
            ->section('content');
    }
}

<?php

namespace App\Modules\SinhVien\Http\Livewire;

use App\Modules\SinhVien\Models\SinhVien;
use Livewire\Component;

class SinhVienIndex extends Component
{
    public array $sinhViens = [];

    public function mount()
    {
        $this->sinhViens = SinhVien::with('lop.nganh.khoa')->get()->toArray();
    }

    public function render()
    {
        return view('livewire.sinh-vien.index')
            ->extends('layouts.app')
            ->section('content');
    }
}

<?php

namespace App\Modules\SinhVien\Http\Livewire;

use App\Modules\SinhVien\Models\SinhVien;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class SinhVienProfile extends Component
{
    public ?array $student = null;

    public function mount()
    {
        $user = Auth::guard('student')->user();
        $this->student = SinhVien::with('lop.nganh.khoa')->find($user->MaSV)?->toArray();
    }

    public function render()
    {
        return view('livewire.sinh-vien.profile')
            ->extends('layouts.app')
            ->section('content');
    }
}

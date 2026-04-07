<?php

namespace App\Modules\ThongBao\Http\Livewire\Student;

use App\Modules\ThongBao\Services\ThongBaoService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class ThongBaoList extends Component
{
    public array $thongBaos = [];
    public int $chuaDocCount = 0;

    public function mount(ThongBaoService $service)
    {
        $user = Auth::guard('student')->user();
        $this->thongBaos = $service->danhSachThongBao($user->MaSV)->toArray();
        $this->chuaDocCount = $service->danhSachChuaDoc($user->MaSV);
    }

    public function render()
    {
        return view('livewire.thong-bao.student.list')
            ->extends('layouts.app')
            ->section('content');
    }
}

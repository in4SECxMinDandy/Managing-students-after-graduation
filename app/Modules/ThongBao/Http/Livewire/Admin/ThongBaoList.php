<?php

namespace App\Modules\ThongBao\Http\Livewire\Admin;

use App\Modules\ThongBao\Services\ThongBaoService;
use Livewire\Component;

class ThongBaoList extends Component
{
    public array $thongBaos = [];

    public function mount(ThongBaoService $service)
    {
        $this->thongBaos = $service->danhSachGui()->toArray();
    }

    public function render()
    {
        return view('livewire.thong-bao.admin.list')
            ->extends('layouts.app')
            ->section('content');
    }
}

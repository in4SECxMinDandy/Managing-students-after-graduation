<?php

namespace App\Modules\Khoa\Http\Livewire;

use App\Modules\Khoa\Models\Khoa;
use App\Modules\Khoa\Services\KhoaService;
use Livewire\Component;

class KhoaIndex extends Component
{
    public array $khoas = [];

    public function mount(KhoaService $service)
    {
        $this->khoas = $service->all()->toArray();
    }

    public function deleteKhoa(string $maKhoa, KhoaService $service)
    {
        $service->delete($maKhoa);
        $this->khoas = $service->all()->toArray();
        session()->flash('success', 'Xóa khoa thành công!');
    }

    public function render()
    {
        return view('livewire.khoa.index')
            ->extends('layouts.app')
            ->section('content');
    }
}

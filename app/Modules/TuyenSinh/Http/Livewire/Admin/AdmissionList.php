<?php

namespace App\Modules\TuyenSinh\Http\Livewire\Admin;

use App\Modules\TuyenSinh\Services\TuyenSinhService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class AdmissionList extends Component
{
    public array $pendingApplications = [];

    public function mount(TuyenSinhService $service)
    {
        $this->pendingApplications = $service->getPendingApplications()->toArray();
    }

    public function approve(string $maPTXT, TuyenSinhService $service)
    {
        $maAdmin = Auth::guard('admin')->user()->MaAdmin;
        $service->approveApplication($maPTXT, $maAdmin);
        session()->flash('success', 'Đã duyệt hồ sơ!');
        $this->pendingApplications = $service->getPendingApplications()->toArray();
    }

    public function reject(string $maPTXT, TuyenSinhService $service)
    {
        $maAdmin = Auth::guard('admin')->user()->MaAdmin;
        $service->rejectApplication($maPTXT, $maAdmin);
        session()->flash('success', 'Đã từ chối hồ sơ.');
        $this->pendingApplications = $service->getPendingApplications()->toArray();
    }

    public function render()
    {
        return view('livewire.tuyen-sinh.admin.list')
            ->extends('layouts.app')
            ->section('content');
    }
}

<?php

namespace App\Modules\ThongBao\Http\Livewire\Admin;

use App\Modules\Khoa\Models\Khoa;
use App\Modules\Lop\Models\Lop;
use App\Modules\Nganh\Models\Nganh;
use App\Modules\ThongBao\Services\ThongBaoService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class ThongBaoCreate extends Component
{
    public string $noiDung = '';
    public string $loai = 'all';
    public ?string $maKhoa = null;
    public ?string $maNganh = null;
    public ?string $maLop = null;

    public array $khoas = [];
    public array $nganhs = [];
    public array $lops = [];

    public function mount()
    {
        $this->khoas = Khoa::all()->toArray();
    }

    protected array $rules = [
        'noiDung' => 'required|string|max:1000',
        'loai' => 'required|in:all,khoa,nganh,lop',
    ];

    protected array $messages = [
        'noiDung.required' => 'Nội dung thông báo là bắt buộc.',
        'noiDung.max' => 'Nội dung không được quá 1000 ký tự.',
        'loai.required' => 'Loại thông báo là bắt buộc.',
    ];

    public function updatedLoai(string $value)
    {
        if ($value === 'khoa') {
            $this->nganhs = [];
            $this->lops = [];
        } elseif ($value === 'nganh') {
            $this->nganhs = Nganh::all()->toArray();
            $this->lops = [];
        } elseif ($value === 'lop') {
            $this->nganhs = Nganh::all()->toArray();
            $this->lops = Lop::all()->toArray();
        }
    }

    public function send(ThongBaoService $service)
    {
        $this->validate();

        $maAdmin = Auth::guard('admin')->user()->MaAdmin;
        $service->guiThongBao($this->noiDung, $maAdmin, $this->loai);

        session()->flash('success', 'Gửi thông báo thành công!');
        $this->reset(['noiDung', 'loai', 'maKhoa', 'maNganh', 'maLop']);
    }

    public function render()
    {
        return view('livewire.thong-bao.admin.create')
            ->extends('layouts.app')
            ->section('content');
    }
}

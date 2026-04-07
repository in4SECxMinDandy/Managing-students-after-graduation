<?php

namespace App\Modules\TuyenSinh\Services;

use App\Modules\SinhVien\Models\SinhVien;
use App\Modules\TuyenSinh\Models\HSOXetTuyen;
use App\Modules\TuyenSinh\Models\PTXetTuyen;
use App\Modules\TuyenSinh\Models\TKXetTuyen;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class TuyenSinhService
{
    public function registerCandidate(array $data): TKXetTuyen
    {
        return TKXetTuyen::create([
            'MaTK'   => $this->generateMaTK(),
            'Email'  => $data['Email'],
            'MatKhau' => Hash::make($data['MatKhau']),
        ]);
    }

    public function createProfile(string $maTK, array $data): HSOXetTuyen
    {
        return HSOXetTuyen::create([
            'MaHSO' => $this->generateMaHSO(),
            'MaTK'  => $maTK,
            'HoTen' => $data['HoTen'],
            'CCCD'  => $data['CCCD'],
            'SDT'   => $data['SDT'],
        ]);
    }

    public function submitApplication(string $maHSO, array $data): PTXetTuyen
    {
        return PTXetTuyen::create([
            'MaPTXT'    => $this->generateMaPTXT(),
            'MaHSO'     => $maHSO,
            'MaNganh'   => $data['MaNganh'],
            'PhuongThuc' => $data['PhuongThuc'],
            'Diem'      => $data['Diem'],
            'TrangThai' => PTXetTuyen::TRANG_THAI_CHO_DUYET,
        ]);
    }

    public function approveApplication(string $maPTXT, string $maAdmin): bool
    {
        $application = PTXetTuyen::find($maPTXT);
        if (!$application) {
            return false;
        }

        $application->update([
            'TrangThai' => PTXetTuyen::TRANG_THAI_DAU,
            'MaAdmin'   => $maAdmin,
        ]);

        $this->autoCreateSinhVien($application);

        return true;
    }

    public function rejectApplication(string $maPTXT, string $maAdmin): bool
    {
        $application = PTXetTuyen::find($maPTXT);
        if (!$application) {
            return false;
        }

        $application->update([
            'TrangThai' => PTXetTuyen::TRANG_THAI_ROT,
            'MaAdmin'   => $maAdmin,
        ]);

        return true;
    }

    public function autoCreateSinhVien(PTXetTuyen $application): SinhVien
    {
        $hso = $application->hsoXetTuyen;
        $nganh = $application->nganh;

        return SinhVien::create([
            'MaSV'    => $this->generateMaSV(),
            'HoTen'   => $hso->HoTen,
            'NgaySinh' => $hso->NgaySinh ?? now()->subYears(18),
            'Email'   => $hso->tkXetTuyen->Email,
            'MatKhau' => $hso->tkXetTuyen->MatKhau,
            'MaLop'   => null,
            'MaHSO'   => $hso->MaHSO,
        ]);
    }

    public function getPendingApplications()
    {
        return PTXetTuyen::with(['hsoXetTuyen', 'nghanh'])
            ->where('TrangThai', PTXetTuyen::TRANG_THAI_CHO_DUYET)
            ->orderBy('Diem', 'desc')
            ->get();
    }

    private function generateMaTK(): string
    {
        return 'TK' . str_pad(random_int(1, 9999), 4, '0', STR_PAD_LEFT);
    }

    private function generateMaHSO(): string
    {
        return 'HS' . str_pad(random_int(1, 99999), 5, '0', STR_PAD_LEFT);
    }

    private function generateMaPTXT(): string
    {
        return 'PT' . str_pad(random_int(1, 9999999), 10, '0', STR_PAD_LEFT);
    }

    private function generateMaSV(): string
    {
        return 'SV' . date('y') . str_pad(random_int(1, 9999999), 8, '0', STR_PAD_LEFT);
    }
}

<?php

namespace Tests\Feature;

use App\Modules\Auth\Http\Livewire\AdminLogin;
use App\Modules\Auth\Http\Livewire\CandidateLogin;
use App\Modules\Auth\Http\Livewire\StudentLogin;
use App\Modules\QuanTri\Models\QuanTri;
use App\Modules\SinhVien\Models\SinhVien;
use App\Modules\TuyenSinh\Models\TKXetTuyen;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Livewire\Livewire;
use Tests\TestCase;

/**
 * Regression coverage for session guards + Livewire login (BUG: sanctum guard + plain MatKhau + raw Blade routes).
 */
class AuthGuardsRegressionTest extends TestCase
{
    use RefreshDatabase;

    public function test_admin_dashboard_redirects_when_guest(): void
    {
        $this->get(route('admin.dashboard'))
            ->assertRedirect(route('admin.login'));
    }

    public function test_student_area_redirects_when_guest(): void
    {
        $this->get(route('student.dashboard'))
            ->assertRedirect(route('student.login'));
    }

    public function test_candidate_area_redirects_when_guest(): void
    {
        $this->get(route('candidate.dashboard'))
            ->assertRedirect(route('candidate.login'));
    }

    public function test_admin_guard_attempt_uses_mat_khau_column(): void
    {
        QuanTri::create([
            'MaAdmin' => 'AD01',
            'TenDN'   => 'admin',
            'MatKhau' => Hash::make('admin123'),
        ]);

        $this->assertTrue(Auth::guard('admin')->attempt([
            'TenDN'    => 'admin',
            'password' => 'admin123',
        ]));
    }

    public function test_admin_login_livewire_succeeds_with_bcrypt_mat_khau(): void
    {
        QuanTri::create([
            'MaAdmin' => 'AD01',
            'TenDN'   => 'admin',
            'MatKhau' => Hash::make('admin123'),
        ]);

        Livewire::test(AdminLogin::class)
            ->set('tenDN', 'admin')
            ->set('password', 'admin123')
            ->call('login')
            ->assertRedirect(route('admin.dashboard'));
    }

    public function test_admin_login_rejects_wrong_password(): void
    {
        QuanTri::create([
            'MaAdmin' => 'AD01',
            'TenDN'   => 'admin',
            'MatKhau' => Hash::make('admin123'),
        ]);

        Livewire::test(AdminLogin::class)
            ->set('tenDN', 'admin')
            ->set('password', 'wrong-password')
            ->call('login')
            ->assertHasErrors('tenDN');
    }

    public function test_student_login_succeeds(): void
    {
        SinhVien::create([
            'MaSV'     => 'SVTEST0001',
            'HoTen'    => 'Nguyen Van A',
            'NgaySinh' => '2000-01-01',
            'Email'    => 'svtest@example.com',
            'MatKhau'  => Hash::make('secret12'),
            'MaLop'    => null,
            'MaHSO'    => null,
        ]);

        Livewire::test(StudentLogin::class)
            ->set('maSV', 'SVTEST0001')
            ->set('password', 'secret12')
            ->call('login')
            ->assertRedirect(route('student.dashboard'));
    }

    public function test_candidate_login_succeeds(): void
    {
        TKXetTuyen::create([
            'MaTK'    => 'TK01',
            'Email'   => 'cand@example.com',
            'MatKhau' => Hash::make('secret12'),
        ]);

        Livewire::test(CandidateLogin::class)
            ->set('email', 'cand@example.com')
            ->set('password', 'secret12')
            ->call('login')
            ->assertRedirect(route('candidate.dashboard'));
    }

    public function test_admin_session_does_not_unlock_student_routes(): void
    {
        QuanTri::create([
            'MaAdmin' => 'AD01',
            'TenDN'   => 'admin',
            'MatKhau' => Hash::make('admin123'),
        ]);

        Livewire::test(AdminLogin::class)
            ->set('tenDN', 'admin')
            ->set('password', 'admin123')
            ->call('login');

        $this->get(route('student.dashboard'))
            ->assertRedirect(route('student.login'));
    }

    public function test_student_session_does_not_unlock_admin_routes(): void
    {
        SinhVien::create([
            'MaSV'     => 'SVTEST0001',
            'HoTen'    => 'Nguyen Van A',
            'NgaySinh' => '2000-01-01',
            'Email'    => 'svtest@example.com',
            'MatKhau'  => Hash::make('secret12'),
            'MaLop'    => null,
            'MaHSO'    => null,
        ]);

        Livewire::test(StudentLogin::class)
            ->set('maSV', 'SVTEST0001')
            ->set('password', 'secret12')
            ->call('login');

        $this->get(route('admin.dashboard'))
            ->assertRedirect(route('admin.login'));
    }
}

<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Đăng nhập Thí sinh</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <form wire:submit="login">
        <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Email</label>
            <input type="email" wire:model="email"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="VD: tranvan@example.com">
            @error('email') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2">Mật khẩu</label>
            <input type="password" wire:model="password"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('password') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <button type="submit"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 font-medium">
            Đăng nhập
        </button>
    </form>

    <p class="mt-4 text-center text-gray-600">
        Chưa có tài khoản?
        <a href="{{ route('candidate.register') }}" class="text-blue-600 hover:underline">Đăng ký ngay</a>
    </p>
</div>

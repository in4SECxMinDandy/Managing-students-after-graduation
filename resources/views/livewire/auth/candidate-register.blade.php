<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Đăng ký Thí sinh</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <form wire:submit="register">
        <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Email</label>
            <input type="email" wire:model="email"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('email') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label class="block text-gray-700 font-medium mb-2">Mật khẩu</label>
                <input type="password" wire:model="password"
                    class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                @error('password') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
            </div>
            <div>
                <label class="block text-gray-700 font-medium mb-2">Xác nhận mật khẩu</label>
                <input type="password" wire:model="password_confirmation"
                    class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Họ tên</label>
            <input type="text" wire:model="hoTen"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('hoTen') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div class="grid grid-cols-2 gap-4 mb-6">
            <div>
                <label class="block text-gray-700 font-medium mb-2">CCCD (10 số)</label>
                <input type="text" wire:model="cccd" maxlength="10"
                    class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                @error('cccd') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
            </div>
            <div>
                <label class="block text-gray-700 font-medium mb-2">Số điện thoại</label>
                <input type="text" wire:model="sdt" maxlength="10"
                    class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                @error('sdt') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
            </div>
        </div>

        <button type="submit"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 font-medium">
            Đăng ký
        </button>
    </form>

    <p class="mt-4 text-center text-gray-600">
        Đã có tài khoản?
        <a href="{{ route('candidate.login') }}" class="text-blue-600 hover:underline">Đăng nhập</a>
    </p>
</div>

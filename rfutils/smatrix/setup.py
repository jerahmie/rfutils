from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="smatrix-rust",
    version="0.1",
        rust_extensions=[RustExtension("smatrix_rust.smatrix_rust", binding=Binding.PyO3)],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,
)

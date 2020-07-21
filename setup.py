from setuptools import setup
from setuptools.extension import Extension
import os


def mpi_info(cmd):
    import mpi4py

    config = mpi4py.get_config()
    cmd_compile = " ".join([config["mpicc"], "--showme:%s" % cmd])
    out_stream = os.popen(cmd_compile)
    flags = out_stream.read().strip()

    out = [
        p[2:] if p.startswith(('-I', '-L', '-l'))
        else p for p in flags.split()
    ]
    return out


setup(
    name="mpi4jax",
    packages=[
        "mpi4jax",
        "mpi4jax.collective_ops",
        "mpi4jax.cython"
    ],
    long_description="""Jax-mpi provides integration among jax and MPI, so that 
    code containing MPI calls can be correctly jit-compiled through jax.""",
    ext_modules=[
        Extension(
            name="mpi4jax.cython.mpi_xla_bridge",
            sources=["mpi4jax/cython/mpi_xla_bridge.pyx"],
            include_dirs=mpi_info("compile"),
            library_dirs=mpi_info("libdirs"),
            libraries=mpi_info("libs"),
        ),
    ],
    setup_requires=["setuptools>=18.0", "cython>=0.21", "mpi4py>=3.0.1"],
    install_requires=["jax"]
)

import warnings
import logging

import psutil

import numba.cuda


logger = logging.getLogger(__name__)


try:
    import cupy
except ModuleNotFoundError:
    cupy = None
except ImportError as e:
    # Cupy can be a bit fragile; allow running LiberTEM with
    # messed-up installation
    warnings.warn(repr(e), RuntimeWarning)
    cupy = None


def detect():
    cores = psutil.cpu_count(logical=False)
    if cores is None:
        cores = 2

    try:
        cudas = [device.id for device in numba.cuda.gpus]
    except numba.cuda.CudaSupportError as e:
        # Continue running without GPU in case of errors
        # Keep LiberTEM usable with misconfigured CUDA, CuPy or numba.cuda
        # This DOES happen, ask @uellue!
        cudas = []
        logger.info(repr(e))
    return {
        "cpus": list(range(cores)),
        "cudas": cudas
    }


def has_cupy():
    return cupy is not None

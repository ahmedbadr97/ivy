# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.numpy as ivy_np
import ivy.functional.backends.torch as ivy_torch
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


@st.composite
def _dtypes(draw):
    return draw(
        st.shared(
            helpers.list_of_length(
                x=st.sampled_from(
                    tuple(
                        set(ivy_np.valid_float_dtypes).intersection(
                            set(ivy_torch.valid_float_dtypes)
                        )
                    )
                    + (None,)
                ),
                length=1,
            ),
            key="dtype",
        )
    )


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes)
            )
        )
    ),
    num_positional_args=helpers.num_positional_args(fn_name="sigmoid"),
)
def test_torch_sigmoid(
    dtype_and_x,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="sigmoid",
        input=np.asarray(x, dtype=input_dtype),
        out=None,
    )


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes)
            )
        ),
        min_num_dims=1,
    ),
    axis=st.integers(-1, 0),
    dtypes=_dtypes(),
    num_positional_args=helpers.num_positional_args(fn_name="softmax"),
)
def test_torch_softmax(
    dtype_and_x,
    as_variable,
    axis,
    dtypes,
    num_positional_args,
    native_array,
    fw,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="softmax",
        input=np.asarray(x, dtype=input_dtype),
        dim=axis,
        dtype=dtypes[0],
    )


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes)
            )
        )
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.gelu"
    ),
    approximate=st.sampled_from(["none", "tanh"]),
)
def test_torch_gelu(
    dtype_and_x,
    num_positional_args,
    native_array,
    approximate,
    fw,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=False,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="nn.functional.gelu",
        input=np.asarray(x, dtype=input_dtype),
        approximate=approximate,
    )


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes)
            )
        )
    ),
    num_positional_args=helpers.num_positional_args(
        fn_name="functional.frontends.torch.leaky_relu"
    ),
    alpha=st.floats(min_value=0, max_value=1),
)
def test_torch_leaky_relu(
    dtype_and_x,
    num_positional_args,
    fw,
    alpha,
):
    input_dtype, x = dtype_and_x

    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        as_variable_flags=False,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=False,
        fw=fw,
        frontend="torch",
        fn_tree="nn.functional.leaky_relu",
        input=np.asarray(x, dtype=input_dtype),
        negative_slope=alpha,
    )

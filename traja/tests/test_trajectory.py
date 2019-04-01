import pytest

import numpy as np
import numpy.testing as npt
import pandas as pd
from pandas.util.testing import (
    assert_frame_equal,
    assert_index_equal,
    assert_series_equal,
)

import traja

df = traja.generate()


def test_polar_to_z():
    polar = traja.cartesian_to_polar(df.traja.xy)
    z = traja.polar_to_z(*polar)
    z_expected = np.array(
        [
            0.0 + 0.0j,
            1.341_849_04 + 1.629_900_33j,
            2.364_589_15 + 3.553_397_71j,
            2.363_291_49 + 5.468_934_3j,
            0.543_251_41 + 6.347_378_36j,
            -1.267_300_29 + 5.395_314_54j,
            -3.307_575_32 + 5.404_561_59j,
            -5.186_650_15 + 4.448_845_06j,
            -6.697_132_3 + 3.819_402_59j,
            -8.571_192_1 + 3.149_672_85j,
        ]
    )
    npt.assert_allclose(z[:10], z_expected)


def test_cartesian_to_polar():
    xy = df.traja.xy

    r_actual, theta_actual = traja.cartesian_to_polar(xy)
    r_expected = np.array(
        [
            0.0,
            2.111_192_54,
            4.268_245_2,
            5.957_716_76,
            6.370_583_5,
            5.542_153_82,
            6.336_350_73,
            6.833_268_78,
            7.709_696_31,
            9.131_581_09,
        ]
    )
    theta_expected = np.array(
        [
            0.0,
            0.882_026_17,
            0.983_640_28,
            1.162_901_9,
            1.485_417_65,
            1.801_503_14,
            2.119_990_46,
            2.432_616_94,
            2.623_294_56,
            2.789_438_18,
        ]
    )
    npt.assert_allclose(r_actual[:10], r_expected)
    npt.assert_allclose(theta_actual[:10], theta_expected)


def test_expected_sq_displacement():
    ...


def test_traj_from_coords():
    df_copy = df.copy()
    coords = df_copy.traja.xy
    trj = traja.traj_from_coords(coords)
    assert_frame_equal(trj, df)


def test_distance():
    rotated = traja.trajectory.rotate(df, 10).traja.xy[:10]
    distance = traja.distance(rotated, df.traja.xy)
    npt.assert_almost_equal(distance, 183_889.704_033_224_47)


def test_to_shapely():
    actual = traja.to_shapely(df).bounds
    expected = (
        -51.573_467_680_141_19,
        -61.344_658_104_362_91,
        157.391_866_752_472_54,
        67.338_166_443_218_82,
    )
    npt.assert_allclose(actual, expected)


def test_transition_matrix():
    ...


def test_calculate_flow_angles():
    grid_indices = traja.grid_coordinates(df)
    U, V = traja.calculate_flow_angles(grid_indices.values)
    expected = 8.999_999_999_999_996
    npt.assert_equal(U.sum(), expected)


def test_transitions():
    ...


def test_grid_coordinates():
    grid_indices = traja.trajectory.grid_coordinates(df)
    assert "xbin" in grid_indices
    assert "ybin" in grid_indices
    npt.assert_allclose(grid_indices.xbin.mean(), 8.087_912_087_912_088)

    actual = grid_indices[:10].to_numpy()
    expected = np.array(
        [[4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5], [4, 5]]
    )
    npt.assert_equal(actual, expected)


def test_generate():
    expected = np.array(
        [[0.0, 0.0], [1.341_849_04, 1.629_900_33], [2.364_589_15, 3.553_397_71]]
    )
    df = traja.generate()
    npt.assert_allclose(df.traja.xy[:3], expected)


def test_rotate():
    rotated = traja.trajectory.rotate(df, 10).traja.xy[:10]
    expected = np.array(
        [
            [227.154_185_14, 61.487_682_77],
            [225.141_577_63, 60.850_074_01],
            [223.237_002_34, 59.792_514_34],
            [222.195_998_83, 58.184_536_16],
            [223.245_250_52, 56.457_318_54],
            [225.282_375_72, 56.271_189_84],
            [226.989_281_82, 55.153_478_2],
            [229.085_889_98, 54.933_136_36],
            [230.695_722_54, 54.639_549_44],
            [232.632_539_88, 54.181_972_5],
        ]
    )
    npt.assert_allclose(rotated, expected)


def test_rediscretize_points():
    actual = traja.rediscretize_points(df, R=0.1)[:10].to_dict()
    expected = {
        "x": {
            0: 0.0,
            1: 0.063_558_818_710_072_67,
            2: 0.127_117_637_420_145_34,
            3: 0.190_676_456_130_218_05,
            4: 0.254_235_274_840_290_7,
            5: 0.317_794_093_550_363_37,
            6: 0.381_352_912_260_436_05,
            7: 0.444_911_730_970_508_7,
            8: 0.508_470_549_680_581_4,
            9: 0.572_029_368_390_654,
        },
        "y": {
            0: 0.0,
            1: 0.077_202_827_436_436_01,
            2: 0.154_405_654_872_872_03,
            3: 0.231_608_482_309_308_06,
            4: 0.308_811_309_745_744_06,
            5: 0.386_014_137_182_180_03,
            6: 0.463_216_964_618_616,
            7: 0.540_419_792_055_052,
            8: 0.617_622_619_491_488,
            9: 0.694_825_446_927_924,
        },
    }
    assert expected == actual


def test_calc_turn_angle():
    vals = traja.trajectory.calc_turn_angle(df).values
    npt.assert_allclose(
        vals[:10],
        np.array(
            [
                np.nan,
                np.nan,
                11.463_659_59,
                28.038_777_87,
                64.196_861_33,
                53.501_595_42,
                -27.996_948_96,
                27.218_028_24,
                -4.336_064_62,
                -2.957_002_29,
            ]
        ),
    )


def test_calc_angle():
    ...


def test_calc_displacement():
    ...


def test_calc_derivatives():
    ...


def test_calc_heading():
    actual = traja.calc_heading(df)[:10].values
    expected = np.array(
        [
            np.nan,
            50.536_377_13,
            62.000_036_72,
            90.038_814_59,
            154.235_675_92,
            -152.262_728_67,
            179.740_322_37,
            -153.041_649_39,
            -157.377_714,
            -160.334_716_29,
        ]
    )
    npt.assert_allclose(actual, expected)


def test_speed_intervals():
    ...


def test_get_derivatives():
    actual = traja.get_derivatives(df)[:10].to_numpy()
    expected = np.array(
        [
            [np.nan, 0.000_000_00e00, np.nan, np.nan, np.nan, np.nan],
            [
                2.111_192_54e00,
                2.000_000_00e-02,
                1.055_596_27e02,
                2.000_000_00e-02,
                np.nan,
                np.nan,
            ],
            [
                2.178_494_78e00,
                4.000_000_00e-02,
                1.089_247_39e02,
                4.000_000_00e-02,
                1.682_556_04e02,
                4.000_000_00e-02,
            ],
            [
                1.915_537_04e00,
                6.000_000_00e-02,
                9.577_685_18e01,
                6.000_000_00e-02,
                -6.573_943_56e02,
                6.000_000_00e-02,
            ],
            [
                2.020_942_81e00,
                8.000_000_00e-02,
                1.010_471_40e02,
                8.000_000_00e-02,
                2.635_144_27e02,
                8.000_000_00e-02,
            ],
            [
                2.045_610_67e00,
                1.000_000_00e-01,
                1.022_805_33e02,
                1.000_000_00e-01,
                6.166_964_78e01,
                1.000_000_00e-01,
            ],
            [
                2.040_295_99e00,
                1.200_000_00e-01,
                1.020_147_99e02,
                1.200_000_00e-01,
                -1.328_668_92e01,
                1.200_000_00e-01,
            ],
            [
                2.108_154_72e00,
                1.400_000_00e-01,
                1.054_077_36e02,
                1.400_000_00e-01,
                1.696_468_19e02,
                1.400_000_00e-01,
            ],
            [
                1.636_384_47e00,
                1.600_000_00e-01,
                8.181_922_37e01,
                1.600_000_00e-01,
                -1.179_425_61e03,
                1.600_000_00e-01,
            ],
            [
                1.990_135_19e00,
                1.800_000_00e-01,
                9.950_675_93e01,
                1.800_000_00e-01,
                8.843_767_80e02,
                1.800_000_00e-01,
            ],
        ]
    )
    npt.assert_allclose(actual, expected)


def test_coords_to_flow():
    actual = traja.coords_to_flow(df)[:10]
    expected = (
        np.array(
            [
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
                [
                    -51.573_467_68,
                    -37.642_445_38,
                    -23.711_423_09,
                    -9.780_400_79,
                    4.150_621_5,
                    18.081_643_8,
                    32.012_666_09,
                    45.943_688_39,
                    59.874_710_68,
                    73.805_732_98,
                    87.736_755_27,
                    101.667_777_57,
                    115.598_799_87,
                    129.529_822_16,
                    143.460_844_46,
                    157.391_866_75,
                ],
            ]
        ),
        np.array(
            [
                [
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                    -61.344_658_1,
                ],
                [
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                    -47.046_566_49,
                ],
                [
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                    -32.748_474_87,
                ],
                [
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                    -18.450_383_26,
                ],
                [
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                    -4.152_291_64,
                ],
                [
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                    10.145_799_98,
                ],
                [
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                    24.443_891_59,
                ],
                [
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                    38.741_983_21,
                ],
                [
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                    53.040_074_83,
                ],
                [
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                    67.338_166_44,
                ],
            ]
        ),
        np.array(
            [
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    -1.000_000_00e00,
                    6.123_234_00e-17,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    6.123_234_00e-17,
                    -1.000_000_00e00,
                    7.071_067_81e-01,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    -1.224_646_80e-16,
                    -1.000_000_00e00,
                    1.000_000_00e00,
                    2.000_000_00e00,
                    1.110_223_02e-16,
                    -1.608_122_65e-16,
                    -1.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    2.000_000_00e00,
                    2.000_000_00e00,
                    -5.510_910_60e-16,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    -2.000_000_00e00,
                    1.000_000_00e00,
                    -2.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    -1.836_970_20e-16,
                    6.123_234_00e-17,
                    -1.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                    -3.673_940_40e-16,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    1.000_000_00e00,
                    1.224_646_80e-16,
                    -1.000_000_00e00,
                    -2.000_000_00e00,
                    -2.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    6.123_234_00e-17,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    -3.061_617_00e-16,
                    -1.000_000_00e00,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    -1.836_970_20e-16,
                    0.000_000_00e00,
                ],
                [
                    -1.836_970_20e-16,
                    1.292_893_22e00,
                    -1.000_000_00e00,
                    1.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    -6.123_234_00e-17,
                    -1.224_646_80e-16,
                    -2.000_000_00e00,
                    1.000_000_00e00,
                    -1.836_970_20e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    1.000_000_00e00,
                    1.110_223_02e-16,
                    -1.000_000_00e00,
                    2.000_000_00e00,
                    -1.224_646_80e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    2.000_000_00e00,
                    1.000_000_00e00,
                    -1.836_970_20e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    6.123_234_00e-17,
                    1.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    -1.836_970_20e-16,
                    0.000_000_00e00,
                    -1.836_970_20e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    -1.836_970_20e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    -1.836_970_20e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
            ]
        ),
        np.array(
            [
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.224_646_80e-16,
                    1.224_646_80e-16,
                    1.000_000_00e00,
                    1.224_646_80e-16,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.224_646_80e-16,
                    1.707_106_78e00,
                    1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.224_646_80e-16,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    2.220_446_05e-16,
                    1.110_223_02e-16,
                    1.224_646_80e-16,
                ],
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    -3.000_000_00e00,
                    1.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.224_646_80e-16,
                    -1.000_000_00e00,
                    1.000_000_00e00,
                    -2.000_000_00e00,
                    -1.000_000_00e00,
                    2.449_293_60e-16,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    1.000_000_00e00,
                    1.224_646_80e-16,
                    1.224_646_80e-16,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    0.000_000_00e00,
                    -2.000_000_00e00,
                    1.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    1.224_646_80e-16,
                    0.000_000_00e00,
                ],
                [
                    1.000_000_00e00,
                    2.000_000_00e00,
                    -1.000_000_00e00,
                    1.000_000_00e00,
                    2.449_293_60e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.224_646_80e-16,
                    1.000_000_00e00,
                    -1.000_000_00e00,
                    1.224_646_80e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    -1.000_000_00e00,
                    7.071_067_81e-01,
                    1.000_000_00e00,
                    2.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.110_223_02e-16,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    1.000_000_00e00,
                    1.000_000_00e00,
                    -2.414_213_56e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    1.000_000_00e00,
                    -2.000_000_00e00,
                    -2.000_000_00e00,
                    1.224_646_80e-16,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    1.000_000_00e00,
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
                [
                    0.000_000_00e00,
                    -1.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                    0.000_000_00e00,
                ],
            ]
        ),
    )
    npt.assert_allclose(actual, expected)


def test_from_xy():
    expected = traja.from_xy(df.traja.xy).values[:10]
    actual = np.array(
        [
            [0.0, 0.0],
            [1.341_849_04, 1.629_900_33],
            [2.364_589_15, 3.553_397_71],
            [2.363_291_49, 5.468_934_3],
            [0.543_251_41, 6.347_378_36],
            [-1.267_300_29, 5.395_314_54],
            [-3.307_575_32, 5.404_561_59],
            [-5.186_650_15, 4.448_845_06],
            [-6.697_132_3, 3.819_402_59],
            [-8.571_192_1, 3.149_672_85],
        ]
    )
    npt.assert_allclose(expected, actual)
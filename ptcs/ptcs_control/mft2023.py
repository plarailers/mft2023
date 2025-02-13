import logging

from .components.junction import Junction, JunctionConnection
from .components.obstacle import Obstacle
from .components.position import DirectedPosition, UndirectedPosition
from .components.section import Section, SectionConnection
from .components.sensor_position import SensorPosition
from .components.station import Station
from .components.stop import Stop
from .components.train import Train
from .constants import (
    CURVE_RAIL,
    OUTER_CURVE_RAIL,
    STRAIGHT_1_2_RAIL,
    STRAIGHT_1_4_RAIL,
    STRAIGHT_1_6_RAIL,
    STRAIGHT_RAIL,
    WATARI_RAIL_A,
    WATARI_RAIL_B,
    WATARI_RAIL_C,
)
from .control import Control, create_empty_logger


def create_control(logger: logging.Logger | None = None) -> Control:
    if logger is None:
        logger = create_empty_logger()

    control = Control(logger=logger)

    j0 = Junction(id="j0")
    j1 = Junction(id="j1")
    j2 = Junction(id="j2")
    j3 = Junction(id="j3")

    control.add_junction(j0)
    control.add_junction(j1)
    control.add_junction(j2)
    control.add_junction(j3)

    s0 = Section(
        id="s0",
        length=WATARI_RAIL_A + 7.03 + STRAIGHT_RAIL + CURVE_RAIL * 2 + STRAIGHT_RAIL + WATARI_RAIL_A,
    )
    s1 = Section(
        id="s1",
        length=WATARI_RAIL_B
        + STRAIGHT_RAIL * 3
        + CURVE_RAIL * 3
        + STRAIGHT_RAIL * 4
        + CURVE_RAIL
        + STRAIGHT_RAIL * 2
        + 3.67
        + CURVE_RAIL * 2
        + STRAIGHT_1_2_RAIL
        + WATARI_RAIL_B,
    )
    s2 = Section(
        id="s2",
        length=WATARI_RAIL_B + 4.70 + OUTER_CURVE_RAIL * 2 + WATARI_RAIL_B,
    )
    s3 = Section(
        id="s3",
        length=WATARI_RAIL_A
        + STRAIGHT_RAIL * 2
        + OUTER_CURVE_RAIL * 2
        + STRAIGHT_RAIL
        + STRAIGHT_1_2_RAIL
        + OUTER_CURVE_RAIL * 2
        + STRAIGHT_RAIL * 3
        + OUTER_CURVE_RAIL * 2
        + 6.01
        + WATARI_RAIL_A,
    )
    s4 = Section(
        id="s4",
        length=WATARI_RAIL_C + 4.05 + WATARI_RAIL_C,
    )
    s5 = Section(
        id="s5",
        length=WATARI_RAIL_C,
    )

    control.add_section(s0)
    control.add_section(s1)
    control.add_section(s2)
    control.add_section(s3)
    control.add_section(s4)
    control.add_section(s5)

    A, B = SectionConnection.A, SectionConnection.B
    THROUGH, DIVERGING, CONVERGING = (
        JunctionConnection.THROUGH,
        JunctionConnection.DIVERGING,
        JunctionConnection.CONVERGING,
    )
    control.connect(s0, A, j0, THROUGH)
    control.connect(s0, B, j3, THROUGH)
    control.connect(s1, A, j3, CONVERGING)
    control.connect(s1, B, j0, CONVERGING)
    control.connect(s2, A, j1, CONVERGING)
    control.connect(s2, B, j2, CONVERGING)
    control.connect(s3, A, j2, THROUGH)
    control.connect(s3, B, j1, THROUGH)
    control.connect(s4, A, j0, DIVERGING)
    control.connect(s4, B, j1, DIVERGING)
    control.connect(s5, A, j2, DIVERGING)
    control.connect(s5, B, j3, DIVERGING)

    t0 = Train(
        id="t0",
        min_input=200,
        max_input=250,
        max_speed=40.0,
        length=14.0,
        delta_per_motor_rotation=0.4553 * 0.9 * 0.9,
        head_position=DirectedPosition(
            section=s3,
            target_junction=j1,
            mileage=WATARI_RAIL_A + STRAIGHT_RAIL * 0.5,
        ),
    )
    t1 = Train(
        id="t1",
        min_input=150,
        max_input=210,
        max_speed=40.0,
        length=14.0,
        delta_per_motor_rotation=0.4021,
        head_position=DirectedPosition(
            section=s3,
            target_junction=j1,
            mileage=WATARI_RAIL_A + STRAIGHT_RAIL * 2 + OUTER_CURVE_RAIL * 2 + STRAIGHT_RAIL,
        ),
    )
    t2 = Train(
        id="t2",
        min_input=150,
        max_input=230,
        max_speed=40.0,
        length=14.0,
        delta_per_motor_rotation=0.5048,
        head_position=DirectedPosition(
            section=s3,
            target_junction=j1,
            mileage=WATARI_RAIL_A
            + STRAIGHT_RAIL * 2
            + OUTER_CURVE_RAIL * 2
            + STRAIGHT_RAIL
            + STRAIGHT_1_2_RAIL
            + OUTER_CURVE_RAIL * 2
            + STRAIGHT_RAIL,
        ),
    )
    t3 = Train(
        id="t3",
        min_input=190,
        max_input=220,
        max_speed=40.0,
        length=14.0,
        delta_per_motor_rotation=0.4208,
        head_position=DirectedPosition(
            section=s3,
            target_junction=j1,
            mileage=WATARI_RAIL_A
            + STRAIGHT_RAIL * 2
            + OUTER_CURVE_RAIL * 2
            + STRAIGHT_RAIL
            + STRAIGHT_1_2_RAIL
            + OUTER_CURVE_RAIL * 2
            + STRAIGHT_RAIL * 3
            + OUTER_CURVE_RAIL * 2,
        ),
    )
    t4 = Train(
        id="t4",
        min_input=180,
        max_input=230,
        max_speed=40.0,
        length=40.0,
        delta_per_motor_rotation=0.4241 * 2.2,
        head_position=DirectedPosition(
            section=s1,
            target_junction=j0,
            mileage=WATARI_RAIL_B + STRAIGHT_RAIL * 4,
        ),
    )

    # control.add_train(t0)
    control.add_train(t1)
    control.add_train(t2)
    control.add_train(t3)
    # control.add_train(t4)

    stop_0 = Stop(
        id="stop_0",
        position=DirectedPosition(
            section=s3,
            target_junction=j1,
            mileage=WATARI_RAIL_A + STRAIGHT_RAIL - STRAIGHT_1_6_RAIL,
        ),
    )
    stop_1 = Stop(
        id="stop_1",
        position=DirectedPosition(
            section=s3,
            target_junction=j1,
            mileage=WATARI_RAIL_A
            + STRAIGHT_RAIL * 2
            + OUTER_CURVE_RAIL * 2
            + STRAIGHT_RAIL
            + STRAIGHT_1_2_RAIL
            + OUTER_CURVE_RAIL * 2
            + STRAIGHT_RAIL * 2
            - STRAIGHT_1_6_RAIL,
        ),
    )

    control.add_stop(stop_0)
    control.add_stop(stop_1)

    station_0 = Station(id="station_0", stops=[stop_0])
    station_1 = Station(id="station_1", stops=[stop_1])

    control.add_station(station_0)
    control.add_station(station_1)

    position_173 = SensorPosition(
        id="position_173",
        section=s1,
        target_junction=j0,
        mileage=WATARI_RAIL_B
        + STRAIGHT_RAIL * 3
        + CURVE_RAIL * 3
        + STRAIGHT_RAIL * 4
        + CURVE_RAIL
        + STRAIGHT_RAIL * 2
        + 3.67
        + CURVE_RAIL * 2,
    )
    position_138 = SensorPosition(
        id="position_138",
        section=s3,
        target_junction=j1,
        mileage=WATARI_RAIL_A
        + STRAIGHT_RAIL * 2
        + OUTER_CURVE_RAIL * 2
        + STRAIGHT_RAIL
        + STRAIGHT_1_2_RAIL
        + OUTER_CURVE_RAIL * 2
        + STRAIGHT_RAIL * 3
        + OUTER_CURVE_RAIL * 2,
    )
    position_80 = SensorPosition(
        id="position_80",
        section=s0,
        target_junction=j3,
        mileage=WATARI_RAIL_A + 7.03 + STRAIGHT_RAIL + CURVE_RAIL * 2,
    )
    position_255 = SensorPosition(
        id="position_255",
        section=s2,
        target_junction=j2,
        mileage=WATARI_RAIL_B + 4.70 + OUTER_CURVE_RAIL,
    )
    position_53 = SensorPosition(
        id="position_53",
        section=s3,
        target_junction=j1,
        mileage=WATARI_RAIL_A
        + STRAIGHT_RAIL * 2
        + OUTER_CURVE_RAIL * 2
        + STRAIGHT_RAIL
        + STRAIGHT_1_2_RAIL
        + OUTER_CURVE_RAIL,
    )
    position_99 = SensorPosition(
        id="position_99",
        section=s1,
        target_junction=j0,
        mileage=WATARI_RAIL_B + STRAIGHT_RAIL * 3 + CURVE_RAIL * 3 + STRAIGHT_RAIL * 4 + CURVE_RAIL,
    )
    position_84 = SensorPosition(
        id="position_84",
        section=s1,
        target_junction=j0,
        mileage=WATARI_RAIL_B + STRAIGHT_RAIL * 3 + CURVE_RAIL,
    )

    control.add_sensor_position(position_173)
    control.add_sensor_position(position_138)
    control.add_sensor_position(position_80)
    control.add_sensor_position(position_255)
    control.add_sensor_position(position_53)
    control.add_sensor_position(position_99)
    control.add_sensor_position(position_84)

    obstacle_0 = Obstacle(
        id="obstacle_0",
        position=UndirectedPosition(
            section=s3,
            mileage=WATARI_RAIL_A + STRAIGHT_RAIL * 2,
        ),
        is_detected=False,
    )

    control.add_obstacle(obstacle_0)

    control.verify()
    return control

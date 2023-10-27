
from typing import Self

import glm
from component.rigid_body_component import RigidBodyComponent
from physics.collision_tests import CollisionResult, CollisionTests
from physics.solvers.solver import Solver

from scene.scene_object import SceneObject


class PhysicsWorld:
    """
    Handles all physics interactions between objects
    """

    def __init__(self: Self) -> None:
        self.objects: list[SceneObject] = []  # SceneObjects registered for physics shizzle
        self.solvers: list[Solver] = []  # global physics solvers (gravity, wind etc)
        pass

    def physics_tick(self: Self, delta: float) -> None:
        # run all solvers
        self.solve(delta)
        # get all collisions
        collisions = self.detect_collisions()
        # resolve all found collisions
        self.resolve_collisions(collisions)

    def solve(self: Self, delta: float) -> None:
        for solver in self.solvers:
            for obj in self.objects:
                # run each solver on every registered object
                solver.solve(obj, delta)

    def detect_collisions(self: Self) -> list[CollisionResult]:
        result: list[CollisionResult] = []

        # keep track of objects that have been tested for collision
        # no need to test collisions between the same objects twice
        tested_pairs: dict[SceneObject, list[SceneObject]] = {}

        # for each obj in the world...
        for obj_a in self.objects:
            if obj_a not in tested_pairs:
                tested_pairs[obj_a] = []
            # test against every other object in the world...
            for obj_b in self.objects:
                if obj_b not in tested_pairs:
                    tested_pairs[obj_b] = []
                if obj_a == obj_b: continue  # don't check collision if objects are same
                if obj_b in tested_pairs[obj_a]: continue  # don't check if the pair has already been tested

                # mark this pair as having been tested
                tested_pairs[obj_a].append(obj_b)
                tested_pairs[obj_b].append(obj_a)

                # test the collision
                collision = CollisionTests.test_collision(obj_a, obj_b)

                # if collision test is a hit, add it to the list of collisions
                if collision.is_hit:
                    result.append(collision)

        # returns all hit collisions
        return result

    def resolve_collisions(self: Self, collisions: list[CollisionResult]) -> None:
        for collision in collisions:
            # TODO: resolve collision for both objects (obj_a & obj_b)
            # TODO: seperate objects here (objects shouldn't stay overlapped before resolving)

            # resolve collision for obj_a
            rb_a = collision.obj_a.get_component(RigidBodyComponent)
            rb_a.acceleration -= collision.hit_normal * glm.length(rb_a.velocity) * 0.9  # 0.9 is current hardcoded magic dampening number, add to rigid body?

    def add_solver(self: Self, solver: Solver) -> None:
        self.solvers.append(solver)

    def register_object(self: Self, object: SceneObject) -> None:
        self.objects.append(object)

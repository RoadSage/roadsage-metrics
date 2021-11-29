<template>
  <div class="row">
    <div class="col-md">
      <q-card class="my-card constrain large-screen-only" flat>
        <q-card-section horizontal>
          <q-card-section class="q-ma-md">
            <div class="text-h6">
              Autonomously warn tailgaters who intrude your safe driving space.
            </div>

            <div class="text-body1 q-mt-xl q-ml-xl">
              <p class="q-my-xl">Autonomous sensing & display</p>

              <p class="q-my-xl">
                Advanced LiDAR technology as being used in self-driving cars
              </p>

              <p class="q-my-xl">
                Autonomous, yet fully customisable to your needs
              </p>
            </div>
            <q-btn
              unelevated
              to="/signup"
              color="accent"
              text-color="white"
              label="Sign Up Now"
              padding="md"
              class="full-width"
            />
          </q-card-section>
          <q-img
            class="col-6 q-ma-md"
            style="border-radius: 50%"
            src="~src\assets\landingCardThree.webp"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

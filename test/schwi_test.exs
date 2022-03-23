defmodule SchwiTest do
  use ExUnit.Case
  doctest Schwi

  test "greets the world" do
    assert Schwi.hello() == :world
  end
end

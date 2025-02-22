package science.atlarge.wta.simulator.model

typealias MachineId = Int

class Machine(
    val id: MachineId,
    val name: String,
    val cluster: Cluster,
    val numberOfCpus: Int,
    val dvfsEnabled: Boolean,
    val normalizedSpeed: Double,
    val TDP: Int
) {
    var powerEfficiency: Double

    init {
        cluster.addMachine(this)
        powerEfficiency = (TDP.toDouble() / numberOfCpus) * normalizedSpeed
    }

    override fun equals(other: Any?): Boolean {
        return this === other
    }

    override fun hashCode(): Int {
        return id.hashCode()
    }

    override fun toString(): String {
        return "Machine(id=$id, name='$name', cluster=${cluster.id}, cpus=$numberOfCpus)"
    }

    fun idString(): String {
        return "Machine(id=$id, name='$name', cluster=${cluster.id})"
    }

}